#!/bin/bash
import wikipedia
import urllib3
import json
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

skill_name = "Search Wikipedia"
wiki_intro = "Here is the Wikipedia entry for "
wiki_summary_outro = " Would you like me to continue reading?"

stop_message = "Okay!"
fallback_message = "The Wikipedia skill can't help you with that. What can I help you with?"
fallback_reprompt = 'What can I help you with?'
exception_message = "Sorry. I cannot help you with that."

class QueryWikipediaHandler(AbstractRequestHandler):
	# Handler for Query Wikipedia Intent.
	def can_handle(self, handler_input):
		return (is_request_type("LaunchRequest")(handler_input) or
			is_intent_name("QueryWikipediaIntent")(handler_input))

	def handle(self, handler_input):
		# Take a query from the user
		query = handler_input
	
		logger.info("In QueryWikipediaHandler")

		# Fetch the first Wikipedia result returned for that query
		wiki_page = wikipedia.page(query)

		# Extract that page's title, summary, and full text
		wiki_title = wiki_page.title
		wiki_summary = wikipedia.summary(query)

		# Collect the intro and summary
		speech = (wiki_intro + wiki_title + wiki_summary + wiki_summary_outro)
	
		handler_input.response_builder.speak(speech).ask(speech)
		return handler_input.response_builder.response


class YesMoreInfoIntentHandler(AbstractRequestHandler):
	# Handler for yes to more info intent.
	def can_handle(self, handler_input):
		# type: (HandlerInput) -> bool
		session_attr = handler_input.attributes_manager.session_attributes
		return (is_intent_name("AMAZON.YesIntent")(handler_input) and
                "query" in session_attr)

	def handle(self, handler_input):
		# type: (HandlerInput) -> Response
		logger.info("In YesMoreInfoIntentHandler")

		attribute_manager = handler_input.attributes_manager
		session_attr = attribute_manager.session_attributes
		_ = attribute_manager.request_attributes["_"]

		wiki_fullpage = wiki_page.content
		speech = wiki_fullpage
		handler_input.response_builder.speak(speech)
		return handler_input.response_builder.response



class FallbackIntentHandler(AbstractRequestHandler):
	# Handler for Fallback Intent.
	# AMAZON.FallbackIntent is only available in en-US locale.
	# This handler will not be triggered except in that locale,
	# so it is safe to deploy on any locale.
	def can_handle(self, handler_input):
	# type: (HandlerInput) -> bool
		return is_intent_name("AMAZON.FallbackIntent")(handler_input)

	def handle(self, handler_input):
		# type: (HandlerInput) -> Response
		logger.info("In FallbackIntentHandler")

		handler_input.response_builder.speak(fallback_message).ask(
            fallback_reprompt)
		return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
	# Handler for Session End.
	def can_handle(self, handler_input):
		# type: (HandlerInput) -> bool
		return is_request_type("SessionEndedRequest")(handler_input)

	def handle(self, handler_input):
		# type: (HandlerInput) -> Response
		logger.info("In SessionEndedRequestHandler")

		logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
		return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
	# Catch all exception handler, log exception and
	# respond with custom message.
	def can_handle(self, handler_input, exception):
		# type: (HandlerInput, Exception) -> bool
		return True

	def handle(self, handler_input, exception):
		# type: (HandlerInput, Exception) -> Response
		logger.info("In CatchAllExceptionHandler")
		logger.error(exception, exc_info=True)

		handler_input.response_builder.speak(exception_message).ask(
            exception_reprompt)

		return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
	# Log the alexa requests.
	def process(self, handler_input):
		# type: (HandlerInput) -> None
		logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
	# Log the alexa responses.
	def process(self, handler_input, response):
		# type: (HandlerInput, Response) -> None
		logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(QueryWikipediaHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
