# drain**pip**e

What is the number 1 enemy of the azure-sdk repo when it comes to possible "poison" upstream packages? The first barrier is having every dependency that we've ever installed available in our development feed.

Wheel Miner` should be placed near the end of your python CI `test` phase. It will crawl a given pip cache location, extracting all downloaded wheels and source distributions. As it discovers these, `Wheel Miner` will extract them to a usable format and dump them in a target location. 
    
At the end of your test run, upload the resulting directory to your build artifacts. Voila, every single package your build used.

