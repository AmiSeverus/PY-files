import unittest

from unittest.mock import patch

import app as fn_to_test


test_data = {
    'returned_names':{"Василий Гупкин", "Геннадий Покемонов", "Аристарх Павлов"},
    'returned_shelfs':{
                        '1': ['2207 876234', '11-2', '5455 028765'],
                        '2': ['10006', '111'],
                        '3': []
                    },
    'data_doc': {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    'returned_doc_info_str': 'passport "2207 876234" "Василий Гупкин"',
}

class TestTask1(unittest.TestCase):
    def setUp(self):
        print("method setUp")


    def tearDown(self):
        print("method tearDown")


    @classmethod
    def setUpClass(cls):
        print('setUpClass - work')


    @classmethod
    def tearDownClass(cls):
        print('tearDownClass - work')


    # def test_check_document_existance(self):
    #     self.assertTrue(fn_to_test.check_document_existance("10006"))
    

    # def test_get_doc_owner_name(self):
    #     self.assertEqual(fn_to_test.get_doc_owner_name("10006"), "Аристарх Павлов")

    
    # def test_get_all_doc_owners_names(self):
    #     self.assertSetEqual(fn_to_test.get_all_doc_owners_names(), test_data['returned_names'])


    # def test_append_doc_to_shelf(self):
    #     self.assertDictEqual(fn_to_test.append_doc_to_shelf('111', '2'), test_data['returned_shelfs'])


    # def test_add_new_shelf(self):
    #     self.assertTupleEqual(fn_to_test.add_new_shelf('5'), ('5', True))


    # def test_show_document_info(self):
    #     self.assertEqual(fn_to_test.show_document_info(test_data['data_doc']),test_data['returned_doc_info_str'])


    # def test_get_doc_shelf(self):
    #     self.assertEqual(fn_to_test.get_doc_shelf('10006'), '2')


    # def test_move_doc_to_shelf(self):
    #     self.assertEqual(fn_to_test.move_doc_to_shelf('10006', '3'), '3')


    # @patch('builtins.input', side_effect=['111', 'passport', 'testTest', '3'])
    # def test_add_new_doc(self, mock_inputs):
    #     self.assertEqual(fn_to_test.add_new_doc(), '3')

    # def test_remove_doc_from_shelf(self):
    #     self.assertIsNone(fn_to_test.remove_doc_from_shelf("10006"))

    # def test_delete_doc(self):
    #     self.assertTupleEqual(fn_to_test.delete_doc('10006'), ('10006', True))

if __name__ == '__main__':
    unittest.main()