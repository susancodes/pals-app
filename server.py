from flask import Flask, render_template, redirect, request, flash, session, jsonify

import requests
import json
import pprint

import os

target_key = os.environ["TARGET_KEY"]

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ABCDEF")


@app.route("/")
def homepage():
	"""Displays webapp/homepage"""

	return render_template('index.html')


@app.route('/target')
def target_product():
	"""using Target API to get product info"""

	product_id = "033317192120"
	id_type = "barcode"

	# headers = {"Authorization": TARGET_KEY}
	# /items/v3/{product_id}{?id_type,store_id,fields,key}
	base_url = "https://api.target.com/items/v3/"
	param_url = "%s?id_type=%s&key=%s&ields=extended_core, ids, descriptions, pos_messages, item_hierarchies, product_hierarchies, geographic_compliance, recall, dimensions, brand, relations, entertainment, restrictions, locations, pricing, availability, in_store_locations, images, variations, reviews, user_attributes, color, size, pattern, license_asset, internal_images, vendor, nutrients, flexible_fulfillment, environmental, pharmacy, limited_segment, prepaid, store_product_type_hierarchy, store_merch_hierarchy, online_product_type_hierarchy, webclass_hierarchy, iac_categories, subscription, online_back_order, online_pre_order, fulfillment, purchase_enticement" % (
		product_id, id_type, target_key)
	final_url = base_url + param_url
	print "FINAL URL: ", final_url

	response = requests.get(final_url)

	response_text = response.json()

	pprint.pprint(response_text)

	return response_text



if __name__ == "__main__":

	# connect_to_db(app)
	PORT = int(os.environ.get("PORT", 5000))
	# DebugToolbarExtension(app)

	DEBUG = "NO_DEBUG" not in os.environ

	app.run(debug=DEBUG, host="0.0.0.0", port=PORT)