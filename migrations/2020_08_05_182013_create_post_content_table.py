from orator.migrations import Migration


class CreatePostContentTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('post_contents') as table:
            table.increments('id')
            table.long_text('text')
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('post_contents')
