class ConfigData:
    GEMINI_API_KEY = "AIzaSyAzVAfzE7fX4_trYHLGhZdnJEMTPWnvg30"

    TABLE_SCHEMA = {
        "customers": {
            "username": "string",
            "name": "string",
            "address": "string",
            "birthdate": "datetime",
            "email": "string",
            "active": "boolean",
            "accounts": ["int"],
            "tier_and_details": {
                "tier_id": {
                    "tier": "string",
                    "benefits": ["string"],
                    "active": "boolean"
                }
            }
        },
        "accounts": {
            "account_id": "int",
            "limit": "int",
            "products": ["string"]
        },
        "transactions": {
            "account_id": "int",
            "transaction_count": "int",
            "bucket_start_date": "datetime",
            "bucket_end_date": "datetime",
            "transactions": [
                {
                    "date": "datetime",
                    "amount": "float",
                    "transaction_code": "string",
                    "symbol": "string",
                    "price": "float",
                    "total": "float"
                }
            ]
        }
    }

    SCHEMA_DESCRIPTION = """
    You are working with a financial MongoDB database. It contains 3 collections: customers, accounts, and transactions.

    1. **customers**: Contains user profile info such as name, email, birthdate, address, and linked account IDs.
    2. **accounts**: Contains financial accounts with credit limits and product types.
    3. **transactions**: Contains detailed buy/sell records per account, including symbol, price, and date.

    You may need to join customers → accounts → transactions to fully answer queries.
    Return only what's asked — no extra formatting or JSON wrappers.
    """

    FEW_SHOT_EXAMPLES = [
        {
            "question": "Which customer has the highest number of accounts?",
            "mongo_query": {
                "collection": "customers",
                "operation": "aggregate",
                "pipeline": [
                    { "$project": { "name": 1, "account_count": { "$size": "$accounts" } } },
                    { "$sort": { "account_count": -1 } },
                    { "$limit": 1 }
                ]
            }
        },
        {
            "question": "Show all transactions of Elizabeth Ray across accounts",
            "mongo_query": {
                "collection": "transactions",
                "operation": "aggregate",
                "pipeline": [
                    {
                        "$match": {
                            "account_id": {
                                "$in": "$session.account_ids"
                            }
                        }
                    }
                ]
            }
        },
        {
            "question": "How many accounts does Elizabeth Ray have?",
            "mongo_query": {
                "collection": "customers",
                "operation": "aggregate",
                "pipeline": [
                    { "$match": { "name": "Elizabeth Ray" } },
                    { "$project": { "num_accounts": { "$size": "$accounts" } } }
                ]
            }
        },
        {
            "question": "What are the products linked to account ID 371138?",
            "mongo_query": {
                "collection": "accounts",
                "operation": "find",
                "filter": { "account_id": 371138 },
                "field": ["products"]
            }
        },
        {
            "question": "List all transactions where AMD was bought.",
            "mongo_query": {
                "collection": "transactions",
                "operation": "find",
                "filter": {
                    "transactions": {
                        "$elemMatch": {
                            "symbol": "amd",
                            "transaction_code": "buy"
                        }
                    }
                },
                "field": ["transactions"]
            }
        },
        {
            "question": "When was the last transaction made for account 716662?",
            "mongo_query": {
                "collection": "transactions",
                "operation": "aggregate",
                "pipeline": [
                    { "$match": { "account_id": 716662 } },
                    { "$unwind": "$transactions" },
                    { "$sort": { "transactions.date": -1 } },
                    { "$limit": 1 },
                    { "$project": { "last_date": "$transactions.date" } }
                ]
            }
        },
        {
            "question": "Give the total amount of AMD shares bought across all accounts.",
            "mongo_query": {
                "collection": "transactions",
                "operation": "aggregate",
                "pipeline": [
                    { "$unwind": "$transactions" },
                    { "$match": { "transactions.symbol": "amd", "transactions.transaction_code": "buy" } },
                    { "$group": { "_id": None, "total_amd_bought": { "$sum": "$transactions.amount" } } },
                    { "$project": { "total_amd_bought": 1 } }
                ]
            }
        },
        {
            "question": "Show the limit of all accounts owned by Elizabeth Ray.",
            "mongo_query": {
                "collection": "customers",
                "operation": "aggregate",
                "pipeline": [
                    { "$match": { "name": "Elizabeth Ray" } },
                    { "$lookup": {
                        "from": "accounts",
                        "localField": "accounts",
                        "foreignField": "account_id",
                        "as": "account_details"
                    }},
                    { "$project": {
                        "limits": "$account_details.limit"
                    }}
                ]
            }
        },
        {
            "question": "Which benefits does Elizabeth Ray have?",
            "mongo_query": {
                "collection": "customers",
                "operation": "aggregate",
                "pipeline": [
                    { "$match": { "name": "Elizabeth Ray" } },
                    { "$project": {
                        "benefits": {
                            "$reduce": {
                                "input": { "$objectToArray": "$tier_and_details" },
                                "initialValue": [],
                                "in": { "$concatArrays": ["$$value", "$$this.v.benefits"] }
                            }
                        }
                    }}
                ]
            }
        },
        {
            "question": "How many customers are there in total?",
            "mongo_query": {
                "collection": "customers",
                "operation": "aggregate",
                "pipeline": [
                    { "$count": "total_customers" }
                ]
            }
        },
        {
            "question": "How many accounts exist in total?",
            "mongo_query": {
                "collection": "accounts",
                "operation": "aggregate",
                "pipeline": [
                    { "$count": "total_accounts" }
                ]
            }
        },
        {
            "question": "Give me the total number of transactions recorded.",
            "mongo_query": {
                "collection": "transactions",
                "operation": "aggregate",
                "pipeline": [
                    { "$unwind": "$transactions" },
                    { "$count": "total_transactions" }
                ]
            }
        },
        {
            "question": "What is the total transaction amount for IBM?",
            "mongo_query": {
                "collection": "transactions",
                "operation": "aggregate",
                "pipeline": [
                    { "$unwind": "$transactions" },
                    { "$match": { "transactions.symbol": "ibm" } },
                    { "$group": { "_id": None, "total_ibm": { "$sum": "$transactions.total" } } },
                    { "$project": { "total_ibm": 1 } }
                ]
            }
        },
        {
            "question": "Which product is linked with the highest number of accounts?",
            "mongo_query": {
                "collection": "accounts",
                "operation": "aggregate",
                "pipeline": [
                    { "$unwind": "$products" },
                    { "$group": { "_id": "$products", "count": { "$sum": 1 } } },
                    { "$sort": { "count": -1 } },
                    { "$limit": 1 },
                    { "$project": { "product": "$_id", "count": 1, "_id": 0 } }
                ]
            }
        }
    ]
