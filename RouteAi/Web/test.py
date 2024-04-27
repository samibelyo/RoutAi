from dash import Dash, Input, Output, html, dcc, State
import dash_bootstrap_components as dbc
import sqlite3
import base64
from dash.exceptions import PreventUpdate
import logging
import dash
import unittest
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from main import dashboard_layout

class TestDashboardLayout(unittest.TestCase):
    def test_dashboard_layout(self):
        layout = dashboard_layout()
        self.assertIsInstance(layout, html.Div)
        self.assertEqual(len(layout.children), 2)
        self.assertIsInstance(layout.children[0], html.H1)
        self.assertIsInstance(layout.children[1], dbc.Container)
        self.assertEqual(len(layout.children[1].children), 3)
        self.assertIsInstance(layout.children[1].children[0], dcc.Markdown)
        self.assertIsInstance(layout.children[1].children[1], html.Br)
        self.assertIsInstance(layout.children[1].children[2], dbc.Card)

if __name__ == '__main__':
    unittest.main()