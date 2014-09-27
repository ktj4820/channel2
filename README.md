Channel2
========

http://channel2.derekkwok.net

Note: Version 2.2 of Channel2 is currently under construction. This message will be removed once branch 2.2 is ready.

Deployment
----------

    > mkvirtualenv channel2-deploy
    (channel2-deploy) > cd deploy
    (channel2-deploy) > pip install -r requirements.txt
    (channel2-deploy) > ansible-playbook -i inventory main.yml    
    (channel2-deploy) > fab deploy:2.1
