# Nesharim brand system

## Fixed details

- Organization: נשרים – המרכז לטיפול באתגרי ההתבגרות
- Phone: 053-766-1500
- Email: office@nesharim.org.il
- Address: רחוב יפו 206, ס-מ 1
- Website: nesharim.org.il

Opening speaker details, exactly:

- חזקי גלבוע
- עו״ס קליני (MSW), מומחה לגילאי
- ההתבגרות והתנהגויות סיכון,
- מייסד ומנהל מרכז ׳נשרים׳.

Closing text, exactly: `לייעוץ ומענה:`, `053-766-1500`, `nesharim.org.il`.

## Defaults

- Audience: parents of adolescents
- Purpose: insight plus a practical takeaway
- Depth: medium to deep
- Tone: personal, engaging, and clear
- Language: Hebrew
- Theme: blue
- Length: usually 10-15 slides

## Assets and colors

Use packaged backgrounds and `assets/paamon-fonts.css`. Backgrounds already contain logo, footer, contact line, and decorative rules. Add only central content.

- Blue theme: blue assets; highlight mint `#78DDB5`.
- Green theme: green assets; highlight navy `#0A1C2F`.
- Full-background text is white; framed-background text is navy.
- Coral `#E06768`: tension or problem framing.
- Mustard `#EBC13A`: occasional secondary accent.
- Use at most one optional accent per slide beyond the theme highlight.

## Typography and spacing

- Font: Paamon, then Heebo, Assistant, Arial, sans-serif.
- H1: 56-72px, weight 700-900.
- H2: 28-40px, weight 500-700.
- Body: 22-26px, weight 400-500.
- Strong body: 24-30px, weight 600-700.
- Spacing tokens: 16, 32, 56, and 80px.
- Center text by default. Keep paragraphs short and at most 800px wide.

## Opening and closing structure

- Opening (layout A, full theme background): lecture title, quieter subtitle, a thin white horizontal divider under the subtitle, then the fixed speaker name and all three lines of credentials above. Add only the central divider; do not duplicate the decorative lines already in the background. Mark it `.speaker-divider` or `data-role="speaker-divider"`.
- Ask if it is unclear whether the user's first supplied slide is the lecture title or the first content slide. Ask only for missing title/subtitle details required for the opening, without reopening finalized content.
- Closing (layout A, full theme background): `לייעוץ ומענה:`, phone `053-766-1500` in mint for the blue theme, then `nesharim.org.il` in white. For the green theme use the theme's navy highlight. Append this after the final content slide; never repurpose the last content slide as the closing.
- Protect phone styling on mobile: include `<meta name="format-detection" content="telephone=no">`, inherit brand colors for any automatic detector links, and check the rendered phone color. Do not assume a reported color difference is proven to be automatic detection.

## Emphasis and hierarchy

Use mint for card top borders by default. Use coral or mustard only as a purposeful local accent, not as a required decoration on every slide. When the user names words to emphasize, color those words only and leave the rest in the base text color.

Prioritize legibility: small coral text on white may need stronger weight or size. If a very fine navy letter outline is requested, keep it minimal and inspect both HTML and PDF; do not claim identical support without checking. Maintain a clear main statement, quieter secondary line, and readable closing line.
