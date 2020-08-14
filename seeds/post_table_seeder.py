from orator.seeds import Seeder
from orator.orm import Factory
from faker import Faker


class PostTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        for i in range(50):
            _id = self.db.table('post_contents').insert_get_id(
                self.post_content_factory(),
            )

            self.db.table('posts').insert(
                self.posts_factory(_id),
            )

    def posts_factory(self, _id):
        fake = Faker()

        return {
            'title': fake.sentence(),
            'image': 'https://source.unsplash.com/random/1600x900',
            'abstract': fake.paragraph(),
            'post_content_id': _id,
        }

    def post_content_factory(self):
        fake = Faker()

        return {
            'text': fake.text(),
        }

