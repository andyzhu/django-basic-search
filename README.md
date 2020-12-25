This is the result of tutorial at https://learndjango.com/tutorials/django-search-tutorial

Forms and Querysets
Ultimately a basic search implementation comes down to a form that will pass along a user query--the actual search itself--and then a queryset that will filter results based on that query.

We could start with either one at this point but'll we configure the filtering first and then the form.

Basic Filtering
In Django a QuerySet is used to filter the results from a database model. Currently our City model is outputting all its contents. Eventually we want to limit the search results page to filter the results outputted based upon a search query.

There are multiple ways to customize a queryset and in fact it's possible to do filtering via a manager on the model itself but...to keep things simple, we can add a filter with just one line. So let's do that!

Here it is, we're updating the queryset method of ListView and adding a hardcoded filter so that only a city with the name of "Boston" is returned. Eventually we will replace this with a variable representing the user search query!

# cities/views.py
class SearchResultsView(ListView):
    model = City
    template_name = 'search_results.html'
    queryset = City.objects.filter(name__icontains='Boston') # new
Refresh the search results page and you'll see only "Boston" is now visible.

Boston

It's also possible to customize the queryset by overriding the get_queryset() method to change the list of cities returned. There's no real advantage to do so in our current case, but I find this approach to be more flexible than just setting queryset attributes.

# cities/views.py
...
class SearchResultsView(ListView):
    model = City
    template_name = 'search_results.html'

    def get_queryset(self): # new
        return City.objects.filter(name__icontains='Boston')
Most of the time the built-in QuerySet methods of filter(), all(), get(), or exclude() will be enough. However there is also a very robust and detailed QuerySet API available as well.

Q Objects
Using filter() is powerful and it's even possible to chain filters together. However often you'll want more complex lookups such as using "OR" which is when it's time to turn to Q objects.

Here's an example where we set the filter to look for a result that matches a city name of "Boston" or a state name that contains with "NY". It's as simple as importing Q at the top of the file and then subtly tweaking our existing query.

# cities/views.py
from django.db.models import Q # new
...

class SearchResultsView(ListView):
    model = City
    template_name = 'search_results.html'

    def get_queryset(self): # new
        return City.objects.filter(
            Q(name__icontains='Boston') | Q(state__icontains='NY')
        )
Refresh your search results page and we can see the result.

Boston and New York

Now let's turn to our search form to replace the current hardcoded values with search query variables.

Forms
Fundamentally a web form is simple: it takes user input and sends it to a URL via either a GET or POST method. However in practice this fundamental behavior of the web can be monstrously complex.

The first issue is sending the form data: where does the data actually go and how do we handle it once there? Not to mention there are numerous security concerns whenever we allow users to submit data to a website.

There are only two options for "how" a form is sent: either via GET or POST HTTP methods.

A POST bundles up form data, encodes it for transmission, sends it to the server, and then receives a response. Any request that changes the state of the database--creates, edits, or deletes data--should use a POST.

A GET bundles form data into a string that is added to the destination URL. GET should only be used for requests that do not affect the state of the application, such as a search where nothing within the database is changing, we're just doing a filtered list view basically.

If you look at the URL after visiting Google.com you'll see your search query in the actual search results page URL itself.

For more information, Mozilla has detailed guides on both sending form data and form data validation that are worth reviewing if you're not already familiar with form basics.

Search Form
But for our purposes, we can add a basic search form to our existing homepage right now. Here's what it looks like. We'll review each part below.

<!-- templates/home.html -->
<h1>HomePage</h1>

<form action="{% url 'search_results' %}" method="get">
  <input name="q" type="text" placeholder="Search...">
</form>
For the form the action specifies where to redirect the user after submission of the form. We're using the URL name for our search results page here. Then we specify the use of get as our method.

Within our single input--it's possible to have multiple inputs or to add a button here if desired--we give it a name q which we can refer to later. Specify the type which is text. And then add a placeholder value to prompt the user.

That's really it! On the homepage now try inputting a search, for example for "san diego".

San Diego

Upon hitting Return you are redirected to the search results page. Note in particular the URL contains our search query http://127.0.0.1:8000/search/?q=san+diego.

San Diego Search Result

However the results haven't changed! And that's because our SearchResultsView still has the hardcoded values from before. The last step is to take the user's search query, represented by q in the URL, and pass it in.

# cities/views.py
...
class SearchResultsView(ListView):
    model = City
    template_name = 'search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = City.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query)
        )
        return object_list
We added a query variable that takes the value of q from the form submission. Then update our filter to use query on both a city name and state. That's it! Refresh the search results page--it still has the same URL with our query--and the result is expected.

San Diego

If you want to compare your code with the official source code, it can be found on Github.

Next Steps
Our basic search is now complete! Maybe you want to add a button on the search form that could be clicked in addition to hitting return? Or perhaps add some form validation?

Beyond filtering with ANDs and ORs there are other factors if we want a Google-quality search, things like relevancy and much more. This talk DjangoCon 2014: From __icontains to search is a good taste of how deep the search rabbit hole can go!