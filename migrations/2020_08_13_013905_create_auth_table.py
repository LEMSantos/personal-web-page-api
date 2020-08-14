from orator.migrations import Migration


class CreateAuthTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('auth') as table:
            table.increments('id')
            table.string('token')
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('auth')
