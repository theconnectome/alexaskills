#!/bin/bash
import wikipedia
import urllib3
import json
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)



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
	
if __name__ == '__main__':
    app.run(debug=True)
