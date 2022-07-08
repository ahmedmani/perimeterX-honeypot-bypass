# perimeterX-honeypot-bypass
 this page describes in detail the process in which this bypass was discovered and developed  




# The problem


![px honeypot](https://i.imgur.com/RrCmeWe.png)

perimeterX runs special js code in order to detect if a user is running a webdriver instance or not (http based browsers are not capable of running js code therefore they wont be able to run the fingerprinting code and end up getting blocked instantley this can also be bypassed aswell)

vanilla selenium binaries are instanlty detected this is probably due to a js variable selenium exposes, since selenium is not a normal chrome instance it lacks a lot of apis normal chrome offers i suspect some  the js tries calling some js apis which results in them failing and thus triggering the honeypot this is easily bypassable by using undetected chromedriver.
undetected chromedriver it is a modified selenium binary that looks like a normal chrome instance and it does not trigger the honeypot

this page is the honeypot its offering a simple click me button (which rareley works without automation :) )


the click and hold button is created dynamically using js with random class names and random ids making it almost impossible to locate using selenium locators (xpath included), however this can be bypassed by using image recoginition but that by itself wont work since they are still monitoring mouse movements in order to tell if it was a human who made the interaction or not this can also be bypassed by using a special algorithm that imitates human mouse behaviour using pyautogui and selenium to locate the button.

the only downside to this aproach however that its not possible to replicate this on several selenium instances since pyautogui will take full controll of the mouse and we only have one :)


this takes us to the second option

# google recaptcha v2
![recap v2](https://i.imgur.com/1TXNY8v.png)

by clicking on try a different method we are presented with a recap v2 this can be solved using third party captcha solving apis but for this to work we need to find the callback function and call it passing the result token as a parameter, 


weirdly enough this does not work and not only that but the request indicated in the picture below is not being made at all this can only indicate that they can tell wether a person called the callback function manually or it was called by google captcha.js

weirdly enough all the other js functions names are obfuscated but the most important function is globaly accessible and neatly called handleCaptcha which is very suspicious  

![](https://i.imgur.com/SAnDPs8.png)

i also noticed a request (below image) being made in both success and failure before the userverify which indicates that the response of this request may lead to successful captcha solving or not 
i also noticed that the post params in the success and failure are very different from each other and thus replicating the successful captcha solving post params for this request may be a way to bypass this honeypot  

![the sus request](https://i.imgur.com/rLnRdEa.png)

after diggin through javascript i found that a function called "sendActivities" (that surprisingly sends activities :) ) is responsible for this request and the unencrypted/uncoded body of the request is stored in variable called e (highlighted in the below image) i noticed it simply carried a device fingerprint along with gpu details etc... you can find the exact value here (https://pastebin.com/ib0uz9zn) i tried changing this variable to what ever the successful captcha solving e was holding while calling the callback function manually and low and behold the captcha was solved successfuly 

![](https://i.imgur.com/hgmMwkR.png)

# implementing the solution in selenium  

all we needed to do now was find a way to change whatever the variable e was holding inside the sendActivities only when the request was going to the weird request url after calling the handleCaptcha function (which is accessible in the global scope) and passing the token as a param,

this was a bit hard to implement in selenium since we need to intercept a local js function and modify its variables, one way to do this was to create a modified js file with the correct e value hardcoded and using a mitmproxy instance sitting between selenium and walmart to pass the modified js file instead of the original one and thats what i did and it worked :)

this is a addon for mitmproxy i used this to serve the local modified file instead of the original  
![](https://i.imgur.com/HaZaPcm.png)


# Conclusion
the above solution was working perfectly however the captcha will only be solved after 3 tries this can be explained that it will only solve captcha after collecting a necessary number of biometrics (leftclickdown, leftclickup etc...), another major weakness is that cookies are not validated on each request meaning we are able to take the validated cookies and use them with http requests, making it possible to make the rest of the http calls using requests and only using selenium when the cookies are expired.

