# Tribune negatives project

## Things related to my work as a 'Digital Drop In' at the State Library of NSW's [DXLab](http://dxlab.sl.nsw.gov.au/)

*The Tribune* was a newspaper published by the Communist Party of Australia. The State Library of NSW holds more than 60,000 negatives and photos from the *Tribune* which document a wide range of political events and social issues from 1964 to 1991.

Here's the [top-level record](http://archival.sl.nsw.gov.au/Details/archive/110037137) for the Tribune collection. I think I'll be working with Series 1-4 which contain the negatives. While many of the negatives have been digitised, only a selection are currently available online. Here's some examples:

* [Tribune negatives of anti-Vietnam War demonstrations, including Australia's first sit down demonstration, Sydney, and a protest outside Central Police Court, Liverpool Street, Sydney, New South Wales, 1965](http://archival.sl.nsw.gov.au/Details/archive/110366605)
* [Tribune negatives including protests against development in Woolloomooloo, and Student Action for Aborigines fundraising folk concert at Paddington Town Hall, Sydney, New South Wales, 1965](http://archival.sl.nsw.gov.au/Details/archive/110370048)
* [Tribune negatives including the Freedom Rides SAFA (Student Action For Aboriginals) Trip 17- 26 February, 1965](http://archival.sl.nsw.gov.au/Details/archive/110366670)

To find all the digitised items you can go to the [Advanced Search](http://archival.sl.nsw.gov.au/search/advanced) page, search for title keywords "Tribune negatives", and check the "digital content" box.

For convenience I've created a [list of items](negatives/digitised_items.md) with digitised images available.

### Metadata

As a first step, I've been working at getting metadata relating to the Tribune collection out of the catalogue and into a form I can do something with.

Here's a CSV-formatted list of [all the series](negatives/csv/tribune_series.csv) in the Tribune collection.

In [this folder](negatives/csv) you'll also find CSV-formatted lists of all items in series 1 - 4. For example, here's the items in [Series 1 Part 1](negatives/csv/series-01-part-01-items.csv).

### Word frequencies

I've started some preliminary playing around with the [frequencies of words and phrases](negatives/title_word_frequencies.md) in item titles.

### Related resources

As well as exploring the negatives, I'm going to see what connections can be made to other collections.

Trove includes the [Sydney *Tribune*](http://trove.nla.gov.au/newspaper/title/1002) from 1939 to 1954 and issues for the next two decades are in the [process of being added](http://trove.nla.gov.au/newspaper/result?l-title=1002&q&l-decade=196). This means there'll be a nice overlap to explore between the negatives and the newspapers.

I've fired up my TroveHarvester and grabbed details of the 28,493 post 1954 articles currently listed on Trove. Note that a lot of these are 'Coming soon' -- so you can't actually get to the articles. But articles from 1965 and 1966 are fully available online. You can grab a [CSV file with all the harvested articles here](trove/data/1496625055/results.csv).

A number of the protests and rallies documented by the Tribune were also the subject of ASIO surveillance. I've previously harvested [details of publicly-available ASIO files](https://github.com/wragge/asio-files) from the National Archives of Australia. It'll be interesting to compare perspectives...





