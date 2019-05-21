#!/bin/bash
import wikipedia
import urllib3
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

@ask.intent("SearchWikipediaIntent")
def query_wikipedia():
	# Take a text query from the user
	query = input ("Query: ")

	# Fetch the first Wikipedia result returned for that query
	wiki_page = wikipedia.page(query)

	# Extract that page's title, summary, and full text
	wiki_title = wiki_page.title
	wiki_summary = wikipedia.summary(query)
	wiki_fullpage = wiki_page.content

	# Print the intro and summary
	return question("Here is the Wikipedia entry for " + wiki_title + ":\n" + wiki_summary + "\n Would you like me to continue reading?\n")

@ask.intent("YesIntent")
def full_page():
	return statement(wiki_fullpage)
	
@ask.intent('AMAZON.StopIntent')
def stop():
	return statement("Goodbye")

@ask.intent('AMAZON.CancelIntent')
def cancel():
	return statement("Goodbye")

@ask.session_ended
def session_ended():
	return "{}", 200
