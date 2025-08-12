GPT-5 connector for Seedling. - 12/08/2025

To use GPT-5 isntead of Kimi K2 please replace the ai_connector.py and the priming_prompt.txt.
The priming prompt needed a little tweak to make GPT-5 aware that it can comment on its own actions by typing outside the command block.
Without that it is still working perfectly, but doesn't say a thing which makes the whole procedure less interesting. :)

THis is the first version, hasn't been tested thoroughly, so there may be some issuses. If that is the case i will upload the fixed ai_connector.

updates: 
- 12/08/25 : This first version is working, but when i have been stress testing it I had issues with hitting timeout limitations and token per minute caps. This happens only when Seedling is trying to build a software with large codebase. The timeout issue has been fixed already, but i have to figure out a solution for the token per minute limitation. Apart from this GPT-5 can use the tool perfectly, i am quite impressed with it!
I will update the GPT-5 connector soon.
