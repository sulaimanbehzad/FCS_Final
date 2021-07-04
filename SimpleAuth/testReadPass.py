# import getpass
# print(getpass.getuser())
# print(getpass.getpass())
# -------------------------------------------- get specific user data
# import pwd
# import sys
#
# username = sys.argv[1]
# user_info = pwd.getpwnam(username)
#
# print ('Username:', user_info.pw_name)
# print ('Password:', user_info.pw_passwd)
# print ('Comment :', user_info.pw_gecos)
# print ('UID/GID :', user_info.pw_uid, '/', user_info.pw_gid)
# print ('Home    :', user_info.pw_dir)
# print ('Shell   :', user_info.pw_shell)



# -------------------------------------------- get all users data
import pwd
import operator

# Load all of the user data, sorted by username
all_user_data = pwd.getpwall()
interesting_users = sorted((u
                            for u in all_user_data
                            if not u.pw_name.startswith('_')),
                            key=operator.attrgetter('pw_name'))

# Find the longest lengths for a few fields
username_length = max(len(u.pw_name) for u in interesting_users) + 1
home_length = max(len(u.pw_dir) for u in interesting_users) + 1

# Print report headers
fmt = '%-*s %4s %-*s %s'
print (fmt % (username_length, 'User',
             'UID',
             home_length, 'Home Dir',
             'Description'))
print ('-' * username_length, '----', '-' * home_length, '-' * 30)

# Print the data
for u in interesting_users:
    print (fmt % (username_length, u.pw_name,
                 u.pw_uid,
                 home_length, u.pw_dir,
                 u.pw_gecos))