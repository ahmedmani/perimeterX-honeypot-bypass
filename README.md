# perimeterX-honeypot-bypass
 this page describes in detail the process in which this bypass was discovered and developed  




# The problem

pic(https://imgur.com/a/3cAwdBO) 

perimeterX runs special js code in order to detect if a user is running a webdriver instance or not (http based browsers are not capable of running js code therefore they wont be able to run the fingerprinting code and end up getting blocked instantley this can also be bypassed aswell)
vanilla selenium binaries are instanlty detected this is probably due to a js variable selenium exposes since selenium is not a normal chrome instance it lacks a lot of apis normal chrome offers i suspect some  the js tries calling some js apis which results in them failing and thus triggering the honeypot this is easily bypassable by using undetected chromedriver it is a modified selenium binary that does not trigger the honeypot

this page is a honeypot its offering a simple click me button (which rareley works without automation :) )


the click and hold button is created dynamically using js with random class names and random ids making it almost impossible to locate using selenium locators (xpath included) however this can be bypassed by using image recoginition but that by itself wont work since they are still monitoring mouse movements in order to tell if it was a human who made the interaction or not this can also be bypassed by using a special algorithm that imitates human mouse behaviour using pyautogui and selenium to locate the button the only downside to this aproach however that its not possible to replicate this on several selenium instances since pyautogui will take full controll of the mouse and we only have one :)


this takes us to the second option

# google recaptcha v2
by clicking on try a different method we are presented with a recap v2 this can be solved using third party captcha solving apis but for this to work we need to find the callback function and call it passing the result token as a parameter weirdly enough this does not work and not only that but the request indicated in the third picture is not being made at all this can only indicate that they can tell wether a person called the callback function manually weirdly enough all the other js functions names are obfuscated but the most important function is neatly called handleCaptcha which is very suspicious  


i also noticed a request (third image) being made in both success and failure before the userverify which indicates that the response of this request may lead to successful captcha solving or not 
i also noticed that the post params in the success and failure are very different from each other and thus replicating the successful captcha solving post params for this request may be a way to bypass this honeypot  

after diggin through javascript i found that a function called "sendActivities" (that surprisingly sends activities :) ) is responsible for this request and the unencrypted/uncoded body of the request is stored in variable called e (highlighted in the second image) i noticed it simply carried a device fingerprint along with gpu details etc... you can find the exact value here (https://pastebin.com/ib0uz9zn) i tried changing this variable to what ever the successful captcha solving e was holding while calling the callback function manually and low and behold the captcha was solved successfuly 


# implementing this in selenium      
all we needed to do now was find a way to change whatever the variable e was holding after calling the handleCaptcha function (which is accessible in the global scope) and passing the token as a param,
this was a bit hard to implement in selenium since we need to intercept a local js function and modify its variables, one way to do this was to create a modified js file with the correct e value hardcoded and using a mitmproxy instance sitting between selenium and walmart to pass the modified the js file instead of the original one and thats what i did and it worked :)

the captcha will be solved after 3 tries this can be explained that it will only solve captcha after collecting a necessary number of biometrics (leftclickdown, leftclickup etc...) 

