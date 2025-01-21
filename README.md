
<b><p align='center'>[![Packt Sale](https://static.packt-cdn.com/assets/images/e72907cf-bf2f-4f83-bb58-6cc08a901ff9.jpeg)](https://www.packtpub.com/)</p></b>Get this book on sale at [Packt](https://www.packtpub.com/).

# Learn Grafana 10.x

<a href="https://www.packtpub.com/product/learn-grafana-10x-second-edition/9781803231082"><img src="https://m.media-amazon.com/images/W/MEDIAX_792452-T2/images/I/71kt+Q-vBWL._SL1500_.jpg" alt="Learn Grafana 10.x" height="256px" align="right"></a>

This is the code repository for [Learn Grafana 10.x](https://www.packtpub.com/product/learn-grafana-10x-second-edition/9781803231082), published by Packt.

**A beginner’s guide to practical data analytics, interactive dashboards, and observability**

## What is this book about?

Get ready to unlock the full potential of the open-source Grafana observability platform, ideal for analyzing and monitoring time-series data with this updated second edition. This beginners guide will help you get up to speed with Grafana’s latest features for querying, visualizing, and exploring logs and metrics, no matter where they are stored.

This book covers the following exciting features: 
* Learn the techniques of data visualization using Grafana
* Get familiar with the major components of Time series visualization
* Explore data transformation operations, query inspector, and time interval settings
* Work with advanced dashboard features, such as annotations, variable-based templating, and dashboard linking and sharing
* Connect user authentication through Okta, Google, GitHub, and other external providers
* Discover Grafana’s monitoring support for cloud service infrastructures


If you feel this book is for you, get your [copy](https://www.amazon.in/Learn-Grafana-10-x-interactive-observability/dp/1803231084/ref=sr_1_1?keywords=Learn+Grafana+10.x&sr=8-1) today!

<a href="https://www.packtpub.com/product/data-engineering-with-aws/9781800560413"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders.

The code will look like the following:
```
FROM python:3
SELECT mean("value") FROM "temperature"
WHERE $timeFilter
GROUP BY time($__interval), "station" fill(none)
```
**Following is what you need for this book:**
This book is for business intelligence developers, business analysts, data analysts, and anyone interested in performing time-series data analysis and monitoring using Grafana. You’ll also find this book useful if you’re looking to create and share interactive dashboards or get up to speed with the latest features of Grafana. Although no prior knowledge of Grafana is required, basic knowledge of data visualization and some Python programming experience will help you understand the concepts covered in the book.

With the following software and hardware list you can run all code files present in the book (Chapter 1-17).

### Software and Hardware List

| Chapter  | Software required                                                                    | OS required                        |
| -------- | -------------------------------------------------------------------------------------| -----------------------------------|
|  	1-17	   |   	           Grafana                     			  | Windows, macOS, or Linux | 		
|  	1-17	   |   	                  Docker              			  | Windows, macOS, or Linux | 		
|  	1-17	   |  Loki/Promtail 	                                			  | Windows, macOS, or Linux | 		
|  	1-17	   | Promethues   	                                			  | Windows, macOS, or Linux | 		
|  	1-17	   |   	       InfluxDB/Telegraf                         			  | Windows, macOS, or Linux | 		
|  	1-17	   |   	                        Elasticsearch/Logstash        			  | Windows, macOS, or Linux | 		
|  	1-17	   |   	             OpenLDAP                   			  | Windows, macOS, or Linux | 		
|  	1-17	   |   	                     Python 3.7+           			  | Windows, macOS, or Linux |


### Related products <Other books you may enjoy>
* Alteryx Designer Cookbook  [[Packt]](https://www.packtpub.com/product/alteryx-designer-cookbook/9781804615089) [[Amazon]](https://www.amazon.in/Alteryx-Designer-Cookbook-transform-productivity/dp/1804615080/ref=sr_1_1?keywords=Alteryx+Designer+Cookbook&sr=8-1)
  
* Splunk 9.x Enterprise Certified Admin Guide  [[Packt]](https://www.packtpub.com/product/splunk-9x-enterprise-certified-admin-guide/9781803230238) [[Amazon]](https://www.amazon.in/Splunk-Enterprise-Certified-Admin-Guide/dp/1803230231/ref=tmm_pap_swatch_0?_encoding=UTF8&sr=8-1)
  
## Get to Know the Author
**Eric Salituro** is currently a Software Engineering Manger with the Enterprise Data and Analytics Platform team at Zendesk. He has an IT career spanning over 30 years, over 20 of which were in the motion picture industry working as a pipeline technical director and software developer for innovative and creative studios like DreamWorks, Digital Domain, and Pixar. Before moving to Zendesk, he worked at Pixar helping to manage and maintain their production render farm as a Senior Software Developer. Among his accomplishments there was the development of a Python API toolkit for Grafana aimed at streamlining the creation of rendering metrics dashboards
