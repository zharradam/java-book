// Voyage stations. Quotations are verbatim from manuscript/06-java-leaves-london.md
// (and 03-introduction.md); positions marked approx are estimates for drawing only.
window.JAVA_VOYAGE = [
  { date: "12 October 1839", short: "12 Oct", place: "London", lon: 0.1, lat: 51.5,
    who: "The book", note: "James Trangmar’s diary, as told in the book", text: "He tells us in his diary that he boarded on October 12th 1839, the “JAVA” weighed anchor and was towed down the Thames by a steam tug, to Gravesend, then sailed to the Downs where the anchor was dropped for the night." },
  { date: "18 October 1839", short: "18 Oct", place: "Plymouth", lon: -4.14, lat: 50.37,
    who: "James Trangmar", text: "there has already been some terrible rows amongst them which looks rather bad for a beginning" },
  { date: "28 October 1839", short: "28 Oct", place: "Plymouth Sound", lon: -4.2, lat: 50.33,
    who: "James Trangmar", text: "Hurrah! This morning the Blue Peter is hoisted at the masthead which is the signal for sailing, the sailors call it the Salt Horse Flag. … At 5 o'clock we are once more underway with a fine breeze. Passed the Edystone light and standing well out to sea." },
  { date: "29 October 1839", short: "29 Oct", place: "Off the Scilly Isles", lon: -7.2, lat: 49.8,
    who: "The book", note: "William Richards’ diary, as told in the book", text: "According to William Richards, the “JAVA” passed the Scilly Isles, 40 miles West, on the 29th." },
  { date: "4 November 1839", short: "4 Nov", place: "At sea", lon: -12.5, lat: 39, approx: true,
    who: "William Richards", text: "Fine weather, heavy sea, little wind (child died), an owl lighted in the rigging, starlings, larks and bluebirds caught." },
  { date: "11 November 1839", short: "11 Nov", place: "Canary Islands", lon: -16.5, lat: 28.3,
    who: "William Richards", text: "Passed the Canary Islands, caught the trade winds, child died with whooping cough---very warm." },
  { date: "24 November 1839", short: "24 Nov", place: "5° north of the Line", lon: -24, lat: 5, approx: true,
    who: "James Trangmar", text: "Dead calm, 5 degrees North of the line, rain falling incessantly, buckets, tubs & etc. are in constant use for catching water." },
  { date: "28 December 1839", short: "28 Dec", place: "Rounding the Cape", lon: 20, lat: -39, approx: true,
    who: "William Richards", text: "Strong gale and squally rounding the Cape, gaff cracked in two hail and showers." },
  { date: "28 January 1840", short: "28 Jan", place: "360 miles to go", lon: 128, lat: -36.5, approx: true,
    who: "William Richards", text: "Discovered the main hinge of the rudder broken, rudder supported by chains, wind changed to S.E. 360 miles to go. Child died." },
  { date: "1 February 1840", short: "1 Feb", place: "Fowlers Bay", lon: 132.4, lat: -32.1,
    who: "William Richards", text: "Child to Gahan died. 1 birth, 5pm made land in Fowlers Bay, tacked to South, wind ahead." },
  { date: "6 February 1840", short: "6 Feb", place: "Holdfast Bay", lon: 138.5, lat: -34.98,
    who: "William Richards", text: "Beat the “Rajasthan”, went up the gulf in fine style, anchored in Holdfast Bay, opposite Glenelg 1/4 before 8 a.m. and the “Rajasthan” 20 minutes after us along side, had a shower of rain just after we anchored." },
  { date: "February 1840", short: "Ashore", place: "Holdfast Bay", lon: 138.5, lat: -34.98,
    who: "William Richards", text: "The Governor came aboard, very disgusted at the starving faces of the children, and the languishing women." }
];
window.JAVA_LINKS = {
  read: "read/", passengers: "read/appendix-b-passenger-list-of-the-java.html",
  crew: "read/crew-list-1840-voyage-of-java.html", voyage: "read/java-leaves-london.html",
  epub: "https://github.com/zharradam/java-book/releases/latest/download/the-java.epub",
  pdf: "https://github.com/zharradam/java-book/releases/latest/download/the-java.pdf",
  m4b: "https://github.com/zharradam/java-book/releases/latest/download/the-java.m4b"
};
// Contact link built at runtime so the address is not in the page source
document.addEventListener('DOMContentLoaded', function () {
  var u = 'stephenmichaelbarnett', d = 'gmail.com';
  document.querySelectorAll('[data-contact]').forEach(function (a) {
    a.href = 'mailto:' + u + '@' + d + '?subject=The%20Java'; a.textContent = u + '@' + d;
  });
});
