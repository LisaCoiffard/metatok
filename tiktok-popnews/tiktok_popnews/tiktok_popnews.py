"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import time

from rxconfig import config
from typing import List
from tiktok_popnews.styles import *

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    channels: List[str] = ["https://www.youtube.com/@PopCultureCrisis", "https://www.youtube.com/@popculturenews"]
    video_generated = False
    processing = False
    days_to_cover = "1"
    video = ""
    new_channel: str

    def add_channel(self, form_data: dict[str, str]):
        """Add a new item to the todo list.

        Args:
            form_data: The data from the form.
        """
        # Add the new item to the list.
        self.channels.append(form_data["new_channel"])

        # Clear the value of the input.
        return rx.set_value("new_channel", "")

    def remove_channel(self, channel: str):
        self.channels.pop(self.channels.index(channel))

    def generate_summary(self):
        self.video_generated = False
        self.processing = True

    def process(self):
        time.sleep(1)
        # logic goes here
        self.video_generated = True
        self.processing = False
        self.video = "https://www.youtube.com/watch?v=Syupq6XpAcE"


def new_channel() -> rx.Component:
    return rx.form(
        # Pressing enter will submit the form.
        rx.hstack(
            rx.input(
                id="new_channel",
                placeholder="Add a channel...",
                bg="white",
            ),
            # Clicking the button will also submit the form.
            rx.button("Add", type_="submit", bg="white"),
        ),
        on_submit=State.add_channel,
    )


def channels() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            new_channel(),
            rx.foreach(State.channels, lambda channel: channel_item(channel)),
            width="100%"
        ),
        rx.vstack(
            rx.text("Days to cover: " + State.days_to_cover),
            rx.slider(
                on_change_end=State.set_days_to_cover,
                color_scheme="green",
                default_value=1,
                min_=1,
                max_=7,
            ),
            width="100%"
        ),
        width="100%"
    )


def channel_item(item: rx.Var[str]) -> rx.Component:
    return rx.hstack(
        # A button to finish the item.
        # The item text.
        rx.text(item, font_size="1.25em"),
        rx.button("x",
            on_click=lambda: State.remove_channel(item),
            height="1.5em",
            background_color="white",
            border="1px solid blue",
        ),
    )


def generate_button() -> rx.Component:
    return rx.vstack(
        rx.button(
            rx.text("Generate summary video"),
            _hover={"bg": accent_color},
            style=input_style,
            on_click=[State.generate_summary, State.process],
            width="100%",
        ),
    )


def result() -> rx.Component:
    return rx.vstack(
        rx.cond(
            State.processing,
            rx.circular_progress(is_indeterminate=True),
            rx.cond(
                State.video_generated,
                rx.video(url=State.video, style=video_style),
            ),
        ),
    )


def result2() -> rx.Component:
    return rx.vstack(
        rx.video(url="https://www.youtube.com/watch?v=Syupq6XpAcE", style=video_style),
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Channels"),
            channels(),
            rx.divider(),
            generate_button(),
            rx.divider(),
            result(),
            bg="#ededed",
            margin="5em",
            padding="1em",
            border_radius="0.5em",
            shadow="lg",
            width="100%"
        )
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
