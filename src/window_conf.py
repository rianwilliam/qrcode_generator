"""Perform screen settings"""
from flet import Page

def configure_window(page: Page):
    """
    Determines the default size, minimum screen size of the app

    * Args:
        \t - page (Page): An instance of the page to make the changes
    """
    height = 500
    width = 500

    page.title = "Qr code Generator"
    page.window_maximizable = False
    page.window_width = width
    page.window_height = height
    page.window_min_width = width
    page.window_min_height = height
    page.window_center()
    page.update()
