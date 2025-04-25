# perimeterX-honeypot-bypass
 this page describes the process in which this bypass was developed  




# The problem


![px honeypot](https://i.imgur.com/RrCmeWe.png)

perimeterX runs js code in order to detect if a user is running a webdriver instance or not (not running the js code nor generating a valid solution will result in a block)

vanilla selenium binaries are instanlty detected, this is probably due to some js variables selenium exposes along with unatural mouse movements, since selenium is not a normal chrome instance it lacks a lot of apis normal chrome offers the js could be calling some apis which results in them failing and thus triggering the honeypot this is easily bypassable by using undetected chromedriver.
undetected chromedriver it is a patched selenium binary that behaves like a normal chrome instance and does not automaticaly trigger the honeypot

this page is the honeypot its offering a simple click me button (which rareley works without automation :) )


the click and hold button is created dynamically using js with random class names and random ids making it almost impossible to locate using selenium locators, however this can be bypassed by using image recoginition but that by itself wont work since they are still monitoring mouse movements and js events, in order to tell if it was a human who made the interaction or not. this can also be bypassed using an algorithm that imitates human mouse behaviour using pyautogui and selenium to locate the button. 

the downsides to this aproach however is that its not possible to replicate this on several selenium instances and sooner or later due to browser fingerprinting would result in erroneous solutions. 


this takes us to the second option

# google recaptcha v2
![recap v2](https://i.imgur.com/1TXNY8v.png)

by clicking on try a different method we are presented with a recap v2 this can be solved using third party captcha solving apis but for this to work we need to find the callback function and call it passing the result token as a parameter, 


weirdly enough this does not work, inspecting the requests, the request indicated in the picture below is sent on manual solve, but not being sent when submitting the challenge through js, this indicates js could tell wether a person called the callback function manually or it was called by google captcha.js

after diggin through javascript i found that a function called "sendActivities" (that surprisingly sends activities :) ) is responsible for this request and the unencrypted/uncoded body of the request is stored in variable called e (highlighted in the below image) i noticed it simply carried a device fingerprint along with gpu details etc... you can find the exact value here (https://pastebin.com/ib0uz9zn) i tried changing this variable to what ever the successful captcha solving e was holding, while calling the callback function manually and low and behold the captcha was solved successfuly 

![](https://i.imgur.com/hgmMwkR.png)

# implementing the solution in selenium  

all we need to do now was find a way to change whatever the variable e was holding inside the sendActivities only when the request was going to the weird request url after calling the handleCaptcha function (which is accessible in the global scope) and passing the token as a param,

this was a bit hard to implement in selenium since we need to intercept a local js function and modify its variables, one way to do this was to create a modified js file with the correct e value hardcoded, using a mitmproxy instance sitting between selenium and walmart to pass the modified js file instead of the original one and thats what i did and it worked :)

this is a addon for mitmproxy i used this to serve the local modified file instead of the original  
![](https://i.imgur.com/HaZaPcm.png)


# Conclusion
the above solution was working perfectly however this does not solve the browser fingerprinting problem, this can still be bypassed using a anti detect browser. with the captcha costs and anti detect browser costs, it's better to just use a public solver saving you from a lot of headaches, goodluck

