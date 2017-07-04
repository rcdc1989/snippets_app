import logging
import argparse
import psycopg2

# set the log output file and the log level
logging.basicConfig(filename = "snippets.log", level = logging.DEBUG)
#establish connection to snippets postgreSQL database
logging.debug("Connect to postgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet, hide=False):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    Provides the option to hide snippet from catalog and search functions
    """
    logging.info("storing snippet {!r}: {!r}".format(name,snippet))
    cursor = connection.cursor()
    command = "insert into snippets values(%s,%s)"
    
    #execute query using psycopg2 cursor object
    with connection, connection.cursor() as cursor:
        #check for duplicate records, if one exists, overwrite/update
        try:
            command = "insert into snippets values (%s, %s, %s)"
            cursor.execute(command, (name, snippet, hide))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            command = "update snippets set message=%s, hidden=%s where keyword=%s"
            cursor.execute(command, (snippet, hide, name))
    
    logging.debug("snippet stored successfully")
    return name,snippet
    
def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the snippet.
    """
    
    logging.info("retrieving snippet with keyword {!r}".format(name))
    
    #execute query using psycopg2 cursor object
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword, message from snippets where keyword=%s",
                       (name,)
                      )
        record = cursor.fetchone()

    logging.debug("snippet retrieved successfully")
    
    #handle case where snippet does not exist
    if not record:
        logging.error("Snippet not found")
        return "404: Snippet Not Found"
    
    #return the second element in the tuple
    return record

def catalog():
    """Retrieve a catalog of the available search terms"""
    logging.info("retrieving catalog...")
    
    #execute query for catalog
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets where not hidden order by keyword")
        records = cursor.fetchall()

    logging.debug("retrieved catalog successfully")
    print("snippets are available for the following key words...")
    
    #cycle through list of tuples, printing keywords
    for item in records:
        print(item[0], end = ", ")
    print("\n")
    return records
    
def search(search_term):
    """Search for a snippet by keyword """
    logging.info("searching for keyword " + search_term)
    
    #execute query for catalog using cursor object
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword, message from snippets \
                        where keyword like '%" + search_term + "%' and not hidden")
        records = cursor.fetchall()
    print("found " + str(len(records)) + 
          " records for search term '" + 
          search_term +"'")
    #loop through search results, displaying keyword: message
    for record in records:
        print(record[0] +": "+record[1])
    
    logging.debug("searched for keyword " + search_term)
    print("...")
    return records

################################################################################    
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
    put_parser.add_argument("--hide", action="store_true",
                            help="hide snippet from search and catalog"
                            )
    
    #subparser for the get command
    logging.debug("constructing get subparser")
    get_parser = subparsers.add_parser("get", help = "retrieve a snippet")
    get_parser.add_argument("name", help = "name of desired snippet")
    
    #subparser for the catalog command
    logging.debug("constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", 
                                            help = "retrieve list of keywords")
    
    #subparser for the search command
    logging.debug("constructing search subparser")
    search_parser = subparsers.add_parser("search", 
                                          help = "search for keyword")
    search_parser.add_argument("search_term", 
                               help = "term to search for..")
    
    arguments = parser.parse_args()
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    #excute correct command
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        name, snippet = get(**arguments)
        print("Retrieved snippet: {!r} \n {!r}".format(name, snippet))
    elif command == "catalog":
        print("Retrieved catalog...")
        snippet = catalog()
    elif command == "search":
        snippet = search(**arguments)
        
if __name__=="__main__":
   main()

"""
Notes on error handling:

1->too many arguments gives:
usage: snippets.py [-h] {put,get} ...
snippets.py: error: unrecognized arguments: test3 test3
PASS

2->No arguments gives:
usage: snippets.py put [-h] name snippet
snippets.py put: error: the following arguments are required: name, snippet
PASS

3->unusual datatype for put: 
combinations of lists and dictionaries...all supported
PASS

4->unusual datatype for get: (python3 snippets.py get [1,2,3])
gives: 
Retrieved snippet: '404: Snippet Not Found'
PASS
"""