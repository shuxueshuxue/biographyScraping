import perplexity_tool
import polycli

class Celebrity:
    ...

people = {} # name - celebrity object

name_enumerate_prompt = ""

name_enumerate_agent = polycli.PolyAgent(id="name_thinker")
name_enumerate_agent.run(name_enumerate_prompt, cli="no-tools", model="claude-sonnet-4.5")

# then use perplexity model to find relevant informations (links)
# then use claude code to scrape through these links, (and on demand some extra informations)
# put it in a specific folder
# run it in a loop, each loop is a new celebrity
# these are just raw text materials, but we stop here

