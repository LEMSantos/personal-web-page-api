from orator.seeds import Seeder
from .post_table_seeder import PostTableSeeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(PostTableSeeder)

