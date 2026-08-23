from Eligibility import filter_eligible_schemes

print("Test 1 - should include Micro Finance + AMY (both cap at 1.4L project cost):")
print(filter_eligible_schemes(income=350000, amount_needed=140000, category="SC", purpose="Dairy business"))
print()

print("Test 2 - income too high, should return []:")
print(filter_eligible_schemes(income=600000, amount_needed=100000, category="SC", purpose="Tailoring shop"))
print()

print("Test 3 - exceeds even Term Loan cap, should return []:")
print(filter_eligible_schemes(income=300000, amount_needed=6000000, category="SC", purpose="Factory setup"))
print()

print("Test 4 - education purpose, should ONLY return Education Loan Scheme:")
print(filter_eligible_schemes(income=400000, amount_needed=300000, category="SC", purpose="Engineering course fees"))
print()

print("Test 5 - non-SC category, should return [] regardless of everything else:")
print(filter_eligible_schemes(income=200000, amount_needed=100000, category="OBC", purpose="Small shop"))
print()

print("Test 6 - Term Loan range, should include Term Loan and Udyam Nidhi if under their caps:")
print(filter_eligible_schemes(income=450000, amount_needed=450000, category="SC", purpose="Agriculture expansion"))