import unittest
from unittest.mock import patch, MagicMock, call
import os
import shutil
from src.static_files import copy_to_public

class TestStaticFiles(unittest.TestCase):
    @patch('src.static_files.os.mkdir')
    @patch('src.static_files.shutil.copy')
    @patch('src.static_files.os.listdir')
    @patch('src.static_files.os.path.join', side_effect=os.path.join)
    @patch('src.static_files.os.path.isdir')
    @patch('src.static_files.os.path.exists')
    @patch('src.static_files.shutil.rmtree')
    def test_copy_to_public_check_calls(self, mock_rmtree, mock_exists, mock_isdir, mock_join, mock_listdir, mock_copy, mock_mkdir):
        
        # Define the file structure we are simulating
        # static/
        #   file1.txt
        #   subdir/
        #     file2.txt
        
        exists_responses = {
            "public": [True, False],
        }
        
        def exists_side_effect(path):
            if path == "public":
                if exists_responses["public"]:
                    return exists_responses["public"].pop(0)
                return False # Default after list exhausted
            return False # "public/subdir" doesn't exist, so mkdir called

        mock_exists.side_effect = exists_side_effect
        
        # Listing dirs
        def listdir_side_effect(path):
            if path == "static":
                return ["file1.txt", "subdir"]
            if path == "static/subdir":
                return ["file2.txt"]
            return []
        mock_listdir.side_effect = listdir_side_effect
        
        # IS dir
        def isdir_side_effect(path):
            if path == "static/subdir":
                return True
            return False
        mock_isdir.side_effect = isdir_side_effect
        
        # EXECUTE
        copy_to_public()
        
        # VERIFY
        
        # 1. Cleanup
        mock_rmtree.assert_called_with("public")
        
        # 2. Structure creation
        mock_mkdir.assert_any_call("public")
        mock_mkdir.assert_any_call("public/subdir")
        
        # 3. File copying
        mock_copy.assert_any_call("static/file1.txt", "public/file1.txt")
        mock_copy.assert_any_call("static/subdir/file2.txt", "public/subdir/file2.txt")
        
if __name__ == '__main__':
    unittest.main()
