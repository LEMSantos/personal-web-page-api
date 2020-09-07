from orator.migrations import Migration


class CreatePostTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('posts') as table:
            table.increments('id')
            table.string('title')
            table.string('image')
            table.string('abstract')
            table.integer('post_content_id')
            table.boolean('is_draft').default(False)
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('posts')
