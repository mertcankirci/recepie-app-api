"""
Test custom django management commands 
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error 

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class TestCommands(SimpleTestCase):
    def test_wait_for_db_ready(self, pathced_check):
        
        pathced_check.return_value = True
        
        call_command("wait_for_db")
        
        pathced_check.assert_called_with(databases = ['default'])
    
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_chech):
        
        patched_chech.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
            
        call_command("wait_for_db")
            
        self.assertEqual(patched_chech.call_count, 6)
        patched_chech.assert_called_with(databases = ['default'])
        
        