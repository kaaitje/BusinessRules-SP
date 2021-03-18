from random import randint
import psycopg2

# TODO Change this to your own credentials.
con = psycopg2.connect(database="huwebshop",  # your database name
                       user="postgres",  # your username
                       password="password",  # your password
                       host="localhost",  # your host
                       port=5433)  # normally 5432
cur = con.cursor()


def collaborative_filtering(profid):
    """
    This function looks at the items a profile has viewed, it then looks for profiles who have viewed
    at least one item which the same and it then recommends the other items that profile has viewed.
    :param profid: Profile ID is used to see what items this person has viewed
    :return: Products that the same kind of profiles have viewed
    """
    cur.execute(f"SELECT prodid FROM profiles_previously_viewed WHERE profid = '{profid}';")
    valid = cur.fetchall()
    recommendations = []

    #  Checks if it is a valid prod ID
    if valid:
        #  Takes a random product out of the viewed products
        viewed_prod = valid[randint(0, len(valid) - 1)][0]
        cur.execute(f"SELECT profid FROM profiles_previously_viewed WHERE prodid = '{viewed_prod}';")
        similar_profiles = cur.fetchall()

        #  Keeps track how many times it tried to find a similar profile
        count = 0
        #  Searches profile out of the profiles that watched the same product
        for similar_profile in similar_profiles:
            count += 1
            cur.execute(f"SELECT prodid FROM profiles_previously_viewed WHERE profid = '{similar_profile[0]}'")
            recommendation = cur.fetchone()[0]

            if len(recommendations) < 4:
                if recommendation not in recommendations:
                    try:
                        recommendations.append(cur.fetchone()[0])
                    except TypeError:
                        pass

            #  If he cant find 4 recommendations within 100 tries it switches to content filtering.
            elif count == 100:
                recommendations = content_filtering(viewed_prod)
                return recommendations

            else:
                return recommendations

    else:
        return 'Not a valid profile ID'


def content_filtering(prodid):
    """
    This function takes a product id and recommends related items using the subsub category.
    :param prodid: Product id is used to find products with same subsub category
    :return:
    """
    #  Checks if the ID is an product ID
    cur.execute(f"SELECT id FROM products WHERE id = '{prodid}';")
    valid = cur.fetchone()[0]

    if valid:
        subsubcategory = prod_subsub_cat(prodid)

        #  Searches products with same subsub category
        cur.execute(f"SELECT id FROM products WHERE subsubcategory = '{subsubcategory[0]}'")
        subsub_products = cur.fetchall()

        #  Selects four products with he same subsub category
        recommendations = [subsub_products[randint(0, len(subsub_products) - 1)][0] for _ in range(4)]
        return recommendations
    else:
        return "Not a valid product ID"


def prod_subsub_cat(prodid):
    """
    Simple function that gets the subsub category of a specific product.
    :param prodid: Product id is used to define the product from which we want to get the subsub category
    :return: subsub category
    """
    cur.execute(f"SELECT subsubcategory FROM products WHERE id = '{prodid}';")
    return cur.fetchone()


def product_names(recommendations):
    """
    Simple function that translates the recommended product ID's their names.
    :param recommendations: List of product ID's
    :return: The names of the products
    """
    names = []
    for recommendation in recommendations:
        cur.execute(f"SELECT name FROM products WHERE id = '{recommendation}'")
        names.append(cur.fetchone()[0])
    return names


print(collaborative_filtering("5a393eceed295900010386a8"))
print(content_filtering("7225"))
print(product_names(['45454', '34041', '44207', '36598']))
