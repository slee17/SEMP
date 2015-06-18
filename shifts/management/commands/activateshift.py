from django.core.management.base import BaseCommand, CommandError
from shifts.models import Shift, Sale

class Command(BaseCommand):
	help = 'Activates the specified shift.'

	def add_arguments(self, parser):
		parser.add_argument('shift_id', nargs='+', type=int) # Command-line prompt.

	def handle(self, *args, **options):
		for shift_id in options['shift_id']:
			try:
				shift = Shift.objects.get(pk=shift_id)
			except Shift.DoesNotExist:
				raise CommandError('Shift "%s" does not exist' % shift_id)

			shift.activated = True
			shift.save()

			self.stdout.write('Successfully activated shift "%s".' % shift_id) # Console output.