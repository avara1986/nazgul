# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_http_unit_test]
import unittest
from unittest.mock import Mock

from flask import Flask

import main


class TestNazgul(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_print_test(self):
        user_name = 'test'
        user_id = '1234'
        message = 'test'
        data = {"user": {"displayName": user_name, "name": user_id}, "message": {"text": message}}
        req = Mock(get_json=Mock(return_value=data), args=data)
        with self.app.app_context():
            # Call tested function
            response = main.nazgul_bot(req)
            self.assertEqual(response.json["text"], '{}'.format(message))

    def test_print_name(self):
        user_name = 'prueba'
        user_id = '1234'
        message = 'prueba'
        data = {"user": {"displayName": user_name, "name": user_id}, "message": {"text": message}}
        req = Mock(get_json=Mock(return_value=data), args=data)
        with self.app.app_context():
            # Call tested function
            response = main.nazgul_bot(req)
            self.assertEqual(response.json["text"], '<{}> dijo {}'.format(user_id, message))

    def test_print_help(self):
        user_name = 'test'
        user_id = '1234'
        message = 'help'
        data = {"user": {"displayName": user_name, "name": user_id}, "message": {"text": message}}
        req = Mock(get_json=Mock(return_value=data), args=data)
        with self.app.app_context():
            # Call tested function
            response = main.nazgul_bot(req)
            self.assertEqual(response.json["text"],
                             "*[Saluda, sin más]* Te saluda y te despide\n"
                             "*[Registrar entradas y salidas]* teclea 'r', 'R' o 'registrar' para registrar entrada y salida automáticamente\n"
                             "*[Tiempo invertido esta semana]* Teclea 'horas' para ver cuanto tiempo has invertido cada día\n"
                             "*[Test]* Test\n"
                             "*[Repetir]* Si ninguna acción se detectó, repite el mensaje que llegó\n"
                             )


if __name__ == '__main__':
    unittest.main()
