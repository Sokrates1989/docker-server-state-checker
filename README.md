# serverStateChecker.
Check the state of servers by text files they write themselves.

# Understanding.
The servers create a file with linux server status client https://github.com/Sokrates1989/linux-server-status.git using --json option

The file / the directory of this file are being mapped as volumes to this image. That way this tool gets information about the server.

This image/container (serverStateChecker) should also be created/executed on a similar schedule as the servers cron.

The tool writes regular information into cretain telegram chats/ chatgroups.
If Thresholds are exceeded other measurs can be taken to address the new importance of the information. 
Using a different chat, that uses other -more intrusive- notification settings or an email could be such measurs.

# Environment Vars.
Pass warning and error limits/ thresholds based on the servers capabilities and your requirments in percentages.