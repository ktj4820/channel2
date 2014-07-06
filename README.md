Channel2
========

Deployment
----------

    > mkvirtualenv channel2-deploy
    (channel2-deploy) > cd deploy
    (channel2-deploy) > pip install -r requirements.txt
    (channel2-deploy) > ansible-playbook -i inventory main.yml
    (channel2-deploy) > fab deploy:2.1
