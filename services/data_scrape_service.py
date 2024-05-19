from selenium import webdriver
from bs4 import BeautifulSoup

import networkx as nx
import matplotlib.pyplot as plt
import uuid

from domain.data_scrape import Job, DataScrapeResult, DataScrapeJob
from domain.open_ai import Embedding
from repositories.data_scrape_repository import DataScrapeRepository
from services.open_ai_service import OpenAiService


class DataScrapeService:
    """
    Class given a starting url, and base url, is capable of scraping a website to N levels deep.
    """
    def __init__(self, url, base_url, max_depth):
        self.url = url
        self.base_url = base_url
        self.max_depth = max_depth
        self.reset_dependencies()
        self.open_ai_service = OpenAiService()
        self.data_scrape_repository = DataScrapeRepository()

    def _create_driver(self):
        """
        Creates chrome web driver to grab html.
        :return: Driver
        """
        chromeOptionsRemote = webdriver.ChromeOptions()
        chromeOptionsRemote.add_argument("--headless")
        chromeOptionsRemote.add_argument("--no-sandbox")
        chromeOptionsRemote.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Remote(options=chromeOptionsRemote, command_executor='http://selenium:4444/wd/hub')
        return driver

    def get_page_html(self, url):
        """
        Using the chrome driver grabs urls html and returns it.

        :param url:
        :return:
        """
        self.driver.get(url)
        html = self.driver.page_source
        return html

    def draw_graph(self):
        """
        Used to draw a graph of the sites visited where each node is a given page and edges to new
        nodes are links from a page to a new page.

        :return:
        """
        nx.draw(self.graph, with_labels=True, node_size=200, node_color='skyblue', font_size=10)
        plt.title('Data Scrapper Visual')
        plt.show()


    def reset_dependencies(self):
        """Reinitializes dependencies to run a new scrape job."""
        self.driver = self._create_driver()
        self.graph = nx.DiGraph()
        self.visited = set()

    def add_host_if_needed(self, link):
        """If link doesnt contain hostname in link we adjust it with starting hostname."""
        href = link['href']
        if not href.startswith('http'):
            href = self.url + href
        print(f"parsed url: {href}")
        return href

    def add_links_to_queue(self, links, curr_job, queue, path):
        """Given a webpages links we add them to the queue list if
            1. link is within same host
            2. link hasnt been visited
            3. new link doesnt violate max depth
        """
        for link in links:
            href = self.add_host_if_needed(link)
            print(f"this is the host for hte link: {href}")
            print(f"adding to queue: {href not in self.visited and self.base_url in href and curr_job.depth + 1 < self.max_depth}")
            if (href not in self.visited and
                    self.base_url in href and
                    curr_job.depth + 1 < self.max_depth) :
                job = Job(href=href, depth=curr_job.depth + 1, parent=path)
                queue.add(job)

    def add_edge_to_graph(self, curr_job, path):
        """
        Add a new node to the graph.

        :param curr_job:
        :param path:
        :return:
        """
        if curr_job.parent:
            self.graph.add_edge(curr_job.parent, path)

    async def scrape(self, scrape_id) -> list[DataScrapeResult]:
        """
        We set up a starting job where to start and do a BFS search down the website iteratively.

        We also build a graph along the way.
        :return:
        """
        depth = 0
        parsed_documents = []
        initial_job = Job(href=self.url, depth=depth, parent=None)
        queue: set[Job] = set()
        queue.add(initial_job)
        while queue:
            curr_job = queue.pop()
            print(self.visited)
            try:
                self.visited.add(curr_job.href)
                path = uuid.uuid4().hex[:4]
                # self.add_edge_to_graph(curr_job, path)
                html = self.get_page_html(curr_job.href)
                parser = BeautifulSoup(html, 'html.parser')
                parsed_documents.append(DataScrapeResult(url=curr_job.href, content=parser.get_text(), main_url=self.url))
                links = parser.find_all('a', href=True)
                self.add_links_to_queue(links, curr_job, queue, path)
                print(f"queue {len(queue)} seen {len(self.visited)}")
                await self.data_scrape_repository.update_data_scrape_job(scrape_id, len(queue), len(self.visited), "RUNNING")

            except Exception as e:
                self.visited.add(curr_job.href)
        await self.data_scrape_repository.update_data_scrape_job_status(scrape_id, "FINISHED SCRAPING")
        self.driver.quit()
        return parsed_documents

    async def handle_data_scrape_job(self, data_scrape_job: DataScrapeJob, create_embeddings: bool=False):
        current_job = await self.data_scrape_repository.create_data_scrape_job(data_scrape_job)
        print(current_job)
        parsed_documents: list[DataScrapeResult] = await self.scrape(current_job.id)
        for document in parsed_documents:
            await self.data_scrape_repository.create_data_scrape_job_url(document, data_scrape_job.embeddings_type)
