import sys

from PySide6.QtCore import QObject, Signal, QThread

from PySide6.QtWidgets import QApplication

from nova_ui import NovaUI

from hand_tracking import HandTrackingWorker

from brain import nova_brain

from voice import listen, speak

from computer import computer_command


class AssistantWorker(QObject):

    answer_ready = Signal(str)

    def process(self, command):

        try:

            # Computer commands first
            result = computer_command(command)

            if result:

                self.answer_ready.emit(
                    result
                )

                speak(result)

                return

            # Otherwise use NOVA brain
            answer = nova_brain(
                command
            )

            self.answer_ready.emit(
                answer
            )

            speak(answer)

        except Exception as error:

            message = (
                f"Sorry sir, I encountered "
                f"an error: {error}"
            )

            self.answer_ready.emit(
                message
            )


class NovaApplication:

    def __init__(self):

        self.app = QApplication(
            sys.argv
        )

        self.ui = NovaUI()

        # ------------------------------------------
        # Assistant worker
        # ------------------------------------------

        self.assistant_thread = QThread()

        self.assistant = AssistantWorker()

        self.assistant.moveToThread(
            self.assistant_thread
        )

        self.assistant_thread.start()

        # ------------------------------------------
        # Connect commands
        # ------------------------------------------

        self.ui.command_signal.connect(
            self.process_command
        )

        self.ui.voice_signal.connect(
            self.process_voice
        )

        self.assistant.answer_ready.connect(
            self.ui.show_nova_message
        )

        # ------------------------------------------
        # Hand tracking
        # ------------------------------------------

        self.hand_thread = HandTrackingWorker()

        self.hand_thread.movement.connect(
            self.ui.hand_movement
        )

        self.hand_thread.status.connect(
            self.ui.hand_status.setText
        )

        self.hand_thread.start()

        # ------------------------------------------
        # Web search
        # ------------------------------------------

        self.ui.search_signal.connect(
            self.web_search
        )

        # ------------------------------------------
        # Screenshot
        # ------------------------------------------

        self.ui.screenshot_signal.connect(
            self.take_screenshot
        )

        self.ui.show()

    # ------------------------------------------
    # COMMAND
    # ------------------------------------------

    def process_command(self, command):

        self.ui.chat_title.setText(
            "NOVA // PROCESSING"
        )

        self.assistant.process(
            command
        )

    # ------------------------------------------
    # VOICE
    # ------------------------------------------

    def process_voice(self):

        try:

            command = listen()

            if command:

                self.ui.show_user_message(
                    command
                )

                self.ui.chat_title.setText(
                    "NOVA // PROCESSING"
                )

                self.assistant.process(
                    command
                )

            else:

                self.ui.chat_title.setText(
                    "NOVA // READY"
                )

                self.ui.chat_label.setText(
                    "I didn't catch that, sir."
                )

        except Exception as error:

            self.ui.chat_label.setText(
                f"Voice error: {error}"
            )

    # ------------------------------------------
    # WEB SEARCH
    # ------------------------------------------

    def web_search(self):

        self.ui.input_box.setText(
            "Search the web for..."
        )

        self.ui.input_box.setFocus()

    # ------------------------------------------
    # SCREENSHOT
    # ------------------------------------------

    def take_screenshot(self):

        result = computer_command(
            "take a screenshot"
        )

        if result:

            self.ui.show_nova_message(
                result
            )

    # ------------------------------------------
    # EXIT
    # ------------------------------------------

    def shutdown(self):

        self.hand_thread.stop()

        self.hand_thread.wait(
            2000
        )

        self.assistant_thread.quit()

        self.assistant_thread.wait(
            2000
        )


def main():

    nova = NovaApplication()

    try:

        exit_code = nova.app.exec()

    finally:

        nova.shutdown()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()