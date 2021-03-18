# BusinessRules-SP

Database used: STUDENT VERSION - SP Backup Database 2020-03-12

Pseudo code: Collaborative Filtering
1. Check if the given profid exists
2. Take a random prodid this person previously viewed.
3. Look for other profiles who also viewed this product.
4. Loop through the profiles and add prodid's they've viewed which arent in the recommendation yet until you have 4 id's.
5  Return these prodid's.
6. Use content filtering if you haven't found four profid's within 100 tries.

Psuedo code: Content Filtering
1. Check if the given prodid exists.
2. Use the prodid to find its subsub category.
3. Take four random items from the subsub category
4. Return these recommendations
