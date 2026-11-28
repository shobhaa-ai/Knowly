KNOWLY - RAG Application that will take the documents for specific organization and answere the user queries specific to the documents provided.

Project structure: 

.venv - virtual environment - have dependencies isolated for this specific project
data -> 
    1. processed - contains json files processed from the raw files with list of document structure - document structure is a json object with two fields - page content and metadata
    2. raw - raw files storage that will store the files uploaded by the user
    3. sample - sample of files used for develpment and testing

scripts - this has testing scripts for testing different functionalities
    1. ingest_samples.py - script to test ingesting files of different formats 
        what it does? - take files from sample directory and call ingest_file service to ingest the file
    2. verify_db.py - call init_db() and connect with the engine to check if the tables are created.
    3. chunk_document.py - test the chunk_document service
    4. test_chunking.py - test the chunker.chunk function
src\knowly
    1. api
        1. routes 
            - health.py - gets the session using get_db and executes select 1 query to check if the database is connected
    2. core
        1. config.py - that has the configuration settings - a class is implemented inhering the BaseSettings and an obect of the same is created.
        the properties of the object includes - Appname, groq api key, app env, etc.
    3. db
        1. repositories - it has functions that executes sql queries to interact with database
            document.py - it contains functions interacting with the database
        2. base.py - a class that will be inherited by all the model subclasses
        3. init_db.py - it contains the function that connects with the db engine and create all the tables using the Base class
        4. models.py - contains all the ORM models defined as class in python that inherits the base class and will be used to create tables in db
        5. session.py - creates db engine, session factory and a dependency that provides session, also a listener event function that helps to explicitly implement foreign keys as it is not by default by the sqllite
    4. embeddings
        1. base.py - base class to be inhereted by any embedding model
        2. sentence_transformer.py - embed documents using sentence transformer model
    5. evaluation
    6. generation
    7. ingestion
        1. loaders - contains all the different types of document loaders
            1. html_loader.py - reads the file content - use Beautiful soap to parse the html content - remove the scripts and styles and noscripts - create a list of document structure of this content seperating it into sections on the basis of tags and also adding the section heading.
            2. markdown_loader.py - read the content and provides a list of document structure by segrating it into sections on the basis of headings 
            3. pdf_loader - if the document only has .pdf extension but is actually a text file the it will be read as a text document and a single document structure is returned. otherwise pdfreader will read the file and then create a list of document structure divided on the basis of pages. each page has a seperate document structure.
            4. text_loader.py - it will simply read the file and return a single document structure in the list.
        2. base.py - it is a base class that will be inherited by all the document laoders. it has an abstract method load that compels each loader to have this function implemented.
        3. factory.py - it has a class with get_loader method that gives the loader class dependending on the suffix of the file path
        4. normalizer.py - it nomarlizes the content by removing the extra spaces, tabs, lines and normalizing the mac and windows endlines
        5. service.py - it contains function to ingest file - it creates hash of the file, check for duplicacy, finds the correct loader using get_loader, load the document, normalizes the content, save the raw and processed data and create document record in db.
    8. retrieval
    9. main.py - initialize the fastapi app , lifespan and include routers.
    10. chunking - performs the chunking process
        1. strategies
            1. fixed.py - performs fixed chunking
            2. recursive.py - performs recursive chunking
            3. semantic.py - performs sementic chunking
        2. base.py - base interface that makes a contract for all the chunking strategies to implement function chunk
        3. config.py - it has all the chunking configurations which are used for different chunking strategies including chunk size, chunk overlap, etc.
        4. factory.py - it returns the correct chunker class as per the strategy used
        5. service.py - it implements the chunk_document function irrespective of the chunking strategy used.
        
storage - 
    1. knowly.db - sqllite db
tests 