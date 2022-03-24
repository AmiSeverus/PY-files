import unittest

import app as fn_to_test

# set_all = set()

# from app import check_document_existance, get_doc_owner_name

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
    #     self.assertSetEqual(fn_to_test.get_all_doc_owners_names(), {"Василий Гупкин", "Геннадий Покемонов", "Аристарх Павлов"})


    # def test_remove_doc_from_shelf(self):
    #     self.assertIsNone(fn_to_test.remove_doc_from_shelf("10006"))


    # def test_add_new_shelf(self):
    #     self.assertTupleEqual(fn_to_test.add_new_shelf('5'), ('5', True))


    # def test_append_doc_to_shelf(self):
    #     self.assertDictEqual(fn_to_test.append_doc_to_shelf('111', '2'), {
    #                                                                         '1': ['2207 876234', '11-2', '5455 028765'],
    #                                                                         '2': ['10006', '111'],
    #                                                                         '3': []
    #                                                                     })

    
    # def test_delete_doc(self):
    #     self.assertTupleEqual(fn_to_test.delete_doc('10006'), ('10006', True))


    # def test_get_doc_shelf(self):
    #     self.assertEqual(fn_to_test.get_doc_shelf('10006'), '2')


    def test_move_doc_to_shelf(self):
        self.assertEqual(fn_to_test.move_doc_to_shelf('10006', '3'), '3')

    
if __name__ == '__main__':
    unittest.main()