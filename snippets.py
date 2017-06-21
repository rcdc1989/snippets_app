import logging
import argparse
import psycopg2

# set the log output file and the log level
logging.basicConfig(filename = "snippets.log", level = logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return name
    
def append(name, snippet):
    """
    add to an existing snippet
    Returns the name and the snippet added
    """
    logging.error("FIXME: Unimplemented - append({!r}, {!r})".format(name, snippet))
    return name, snippet
    
def rename(old_name,new_name):
    """
    change name of a snippet to new_name
    """
    logging.error("FIXME: Unimplemented - rename({!r}, {!r})".format(old_name,                                                                  new_name))
    return(new_name)
    
def main():
    """main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")    
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    #subparser for the get command
    logging.debug("constructing get subparser")
    get_parser = subparsers.add_parser("get", help = "retrieve a snippet")
    get_parser.add_argument("name", help = "name of desired snippet")
    
    arguments = parser.parse_args()
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    
if __name__=="__main__":
   main()
    