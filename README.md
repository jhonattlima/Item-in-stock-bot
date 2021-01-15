# Item-in-stock-bot
I created these scripts because I wat trying to buy a new video card. This small script can be used to search for specific buttons in a page (like #add to cart") or if page does not contains a specific sentence anymore (like "out of stock"). When the item gets available, the script sends you an alert mail (you have to configure it before).I hope it helps you.

Explaining how to get the info you need to run the script:

  "link": The full product link;
  "divClassName": The specific class name you want the program to check. If you are using Chrone, press F12 to scan the page and look for this information,
  "type": The type of the item you are scanning. Normally it is a div;
  "stringThatMustNotContain": The strings that must not be contained inside the element you're scanning. Leave it empty if you are only looking if the element is contained inside the page (like an "add to cart" button).
