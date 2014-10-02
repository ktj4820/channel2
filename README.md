Channel2
========

Channel 2 is a personal video hosting service. It allows you to upload, tag and share videos and watch them on other devices.

http://channel2.derekkwok.net

Deployment
----------

Setting up the server

    > mkvirtualenv channel2-deploy
    (channel2-deploy) > cd deploy
    (channel2-deploy) > pip install -r requirements.txt
    (channel2-deploy) > ansible-playbook -i inventory main.yml    
    
Creating a release for deployment

    (channel2-deploy) > git tag -a '2.2.0' -m '2.2.0 release'
    (channel2-deploy) > git push --tags

Deploy

    (channel2-deploy) > fab deploy:2.2.0
