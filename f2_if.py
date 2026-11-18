attendance = "late"
late_fine = 500
absent_fine = 1000
 
if attendance == "present":
    fine = 0
elif attendance == "late":
    fine = late_fine
else:
    fine = absent_fine
print("Fine:", fine)