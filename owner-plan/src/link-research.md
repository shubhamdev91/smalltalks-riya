# Link research: verified URLs and admin paths (checked 2026-10-10)

Method: I checked each URL with curl (HTTP status and final URL after redirects) and read the content with WebFetch. CONFIRMED means the page loads and its content matches the topic. UNCONFIRMED means I could not verify the page or the fact from an official source.
Note: help.shopify.com started returning a Cloudflare 403 to repeated curl requests partway through. Every Shopify page marked CONFIRMED below was still read in full with WebFetch.
Note: this machine geolocates to India (Meta pages report countryCode IN). capcut.com returns HTTP 451 "Unavailable for legal reasons" from here.

## A. Shopify

1. Payments (India)
- Setup guide: https://help.shopify.com/en/manual/payments/third-party-providers/configuring-providers (CONFIRMED)
  - Path: Settings > Payments > in "Payment providers" click "Choose a provider" (the doc's wording when Shopify Payments is unavailable in your country) > pick the provider > enter credentials > Activate > Save. Only the store owner can add a provider. Only one credit-card provider can be active at a time. Some regional methods sit under "Additional payment methods".
- Overview: https://help.shopify.com/en/manual/payments/third-party-providers (CONFIRMED). The old URL .../third-party-providers/setting-up redirects here.
- Gateways by country: https://help.shopify.com/en/manual/payments/third-party-providers/payment-gateway-availability (CONFIRMED). It points to a country filter and does not name Indian gateways.
- Shopify Payments countries: https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries (CONFIRMED). Shopify Payments is available in 40 countries and regions. India is NOT one of them, so the store needs a third-party provider.
- App Store listings (all HTTP 200, checked):
  - Razorpay Secure: https://apps.shopify.com/razorpay-secure (Free to install)
  - PayU India: https://apps.shopify.com/payu-india ("PayU (Cards, UPI, NB, Wallet)", Free to install). Do not use apps.shopify.com/payu, which is "Unzer PayU" (Europe).
  - Cashfree Payments: https://apps.shopify.com/cashfree-payments
- I did not take the Razorpay, PayU or Cashfree setup steps from Shopify docs. The usual flow is: install the app, link the provider account (KYC done), activate in Settings > Payments.

2. Policies: https://help.shopify.com/en/manual/checkout-settings/refund-privacy-tos (CONFIRMED)
- Path: Settings > Policies > "Written policies" > "Return and refund policy" or "Terms of service". Either type your own text (turn "Use automated policy" off) or turn "Use automated policy" on. Click Save. Turning automation on replaces the existing text.

3. Currency formatting: https://help.shopify.com/en/manual/international/pricing/currency-formatting (CONFIRMED)
- Path: Settings > General > "Store defaults" > horizontal menu (three dots) > "Change currency formatting" > edit the fields > Save.
- Format types: "HTML with currency", "HTML without currency", "Email with currency", "Email without currency".
- Supported placeholders include {{amount}}, {{amount_no_decimals}}, {{amount_with_comma_separator}}, {{amount_no_decimals_with_comma_separator}}, {{amount_with_apostrophe_separator}}, {{amount_no_decimals_with_space_separator}}, {{amount_with_space_separator}} and {{amount_with_period_and_space_separator}}.
- ₹{{amount_no_decimals}} is valid syntax and shows as ₹1,135.
- Caveats: the doc does not mention INR or lakh-style grouping (1,00,000). Checkout always shows decimals. The settings apply only to the base currency.

4. Shipping rates: https://help.shopify.com/en/manual/fulfillment/setup/shipping-rates/setting-up-shipping-rates (CONFIRMED)
- Path: Settings > Shipping and delivery > "Shipping profiles" > click the profile (for example General) > horizontal menu next to the rate > "Edit shipping option" > change the Name or price > Done > Save.
- The current docs use "shipping profiles" rather than "General shipping rates".
- Old URLs .../shipping/setting-up-and-managing-your-shipping/... redirect to https://help.shopify.com/en/manual/fulfillment/setup/shipping-rates.

5. Preferences: https://help.shopify.com/en/manual/online-store/setting-up/preferences (CONFIRMED)
- Path: Online Store > Preferences > "Social sharing image and SEO" section > title and meta description > "Add image" for the social sharing image > Save.
- The doc gives no image size.

6. Customer accounts
- Overview: https://help.shopify.com/en/manual/customers/customer-accounts (CONFIRMED). Sign-in is passwordless: the customer gets a one-time 6-digit code by email, and the session lasts up to 365 days. Optional: Shop sign-in and Google/Facebook social sign-in. The old .../new-customer-accounts URL redirects here.
- Manage: https://help.shopify.com/en/manual/customers/customer-accounts/manage (CONFIRMED). Path: Settings > Customer accounts > "Sign-in links" > turn on "Show sign-in links" > Save.
- Sign-in options: https://help.shopify.com/en/manual/customers/customer-accounts/sign-in-options (HTTP 200)
- Upgrade from legacy accounts: https://help.shopify.com/en/manual/customers/customer-accounts/upgrade (link found, content not read)

7. Themes
- Preview: https://help.shopify.com/en/manual/online-store/themes/adding-themes (CONFIRMED). Path: Online Store > "Draft themes" > three-dot menu on the theme > "Preview". The preview bar offers "Close preview" and "Edit theme".
- Publish and roll back: https://help.shopify.com/en/manual/online-store/themes/managing-themes/publishing-themes (CONFIRMED). Path: Online Store > "Draft themes" > "Publish", or from the theme editor: Publish > Publish. Publishing moves the old live theme into Draft themes. To roll back, publish the earlier theme from Draft themes again.
- Also available (link found, not read): https://help.shopify.com/en/manual/online-store/themes/managing-themes/duplicating-themes and .../managing-themes/versions (theme version history).
- Current docs say "Online Store" (the Themes page) for the menu label.

8. Metaobjects: https://help.shopify.com/en/manual/custom-data/metaobjects/creating-entries (CONFIRMED)
- Edit an entry: Content > Metaobjects > click the definition > click the entry > edit > set Draft or Active > Save.
- Add an entry: same path, then "Add entry".
- Hub page: https://help.shopify.com/en/manual/custom-data/metaobjects

9. Facebook & Instagram app
- Setup: https://help.shopify.com/en/manual/online-sales-channels/social-commerce/facebook-instagram-by-meta/setup (CONFIRMED). Old .../online-sales-channels/facebook-instagram-by-meta redirects under /social-commerce/.
  - Path: Settings > Sales channels > Shopify App Store > search Facebook > Add > "Start set up" > "Connect account" > connect the business portfolio, Page, and other assets > accept terms > "Finish setup".
  - The business portfolio must own the Facebook Page.
- Data sharing: https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/meta-data-sharing (CONFIRMED)
  - Levels: "Standard" (pixel only), "Enhanced" (pixel plus Conversions API, sends hashed customer info), "Maximum" (Enhanced plus Meta's latest ad tech).
  - Path: Sales channels > Facebook & Instagram > Settings > Data sharing settings > turn on "Customer data sharing" > "CHOOSE LEVEL".
- Meta pixel: https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/meta-pixel (old .../facebook-pixel redirects here; HTTP 200)
- App listing: https://apps.shopify.com/facebook (HTTP 200)

10. Google & YouTube app
- Connect guide: https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/getting-setup/connect (CONFIRMED)
  - Google account: Sales channels > Google & YouTube > "Connect Google Account".
  - Merchant Center: pick an account from the Merchant Account drop-down (or "Create new"), then complete phone verification.
  - GA4: in the "Looking only to set up Google Analytics 4?" banner, click "Get started" > choose a GA4 property or "Create new" > Connect.
- Hub page: https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google
- Shopify GA setup: https://help.shopify.com/en/manual/reports-and-analytics/google-analytics/google-analytics-setup (HTTP 200)
- App listing: https://apps.shopify.com/google (HTTP 200)

11. Customer privacy and cookie banner: https://help.shopify.com/en/manual/privacy-and-security/privacy/customer-privacy-settings/privacy-settings (CONFIRMED)
- Path: Settings > Customer privacy (admin.shopify.com/settings/privacy) > "Cookie banner" > "Regions and content" (automated or manual) > Position > Save.
- You must publish a privacy policy first.
- In regions where the banner is on, non-essential data and Shopify pixels run only after the visitor consents.
- Manually installed third-party pixels may need their own consent handling.
- The doc says nothing about India or the DPDP Act.
- Pixels overview: https://help.shopify.com/en/manual/promoting-marketing/pixels/overview

12. Analytics and UTM
- Acquisition reports: https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/report-types/default-reports/acquisition-reports (CONFIRMED)
  - Path: Analytics > Reports > Category filter > Acquisition.
  - Reports: Sessions by referrer, Sessions by location, Sessions over time, Visitors over time.
  - Dimensions include Referring channel, Referring platform, Referring medium and Traffic type.
- Marketing reports: https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/report-types/default-reports/marketing-reports (CONFIRMED)
  - Path: Analytics > Reports > Category > Marketing.
  - Reports: Performance by marketing channel, Performance by marketing campaign, Performance by marketing activity, Sales attributed to marketing, Sessions attributed to marketing campaigns.
  - UTM-tagged traffic counts as externally managed marketing.
- Marketing performance (Growth section): https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/marketing-performance (CONFIRMED)
  - Marketing results now live in the "Growth" section (admin.shopify.com/growth).
  - The doc says traffic "with utm_campaign parameters in the URL is attributed to marketing".
  - Attribution models: Last non-direct click (default), Last click, First click, Any click, Linear.
- Reports hub: https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports
- Overview dashboard: https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/overview-dashboard
- No doc states whether these reports are on the Basic plan: UNCONFIRMED.

13. Shopify Forms
- Overview: https://help.shopify.com/en/manual/promoting-marketing/create-marketing/forms-app (CONFIRMED). The doc says the app is "free to install and use" and that you can "add a new or existing discount to a form".
- Create a form: https://help.shopify.com/en/manual/promoting-marketing/create-marketing/forms-app/create (CONFIRMED)
  - First enable the embed: Online Store > Edit theme > App embeds > Forms on > Save.
  - Then: Apps > Forms > "Create form" > Popup or Inline > configure > Save > "Turn form on".
  - The exact click-path for attaching a discount is not on this page: UNCONFIRMED.
- App listing: https://apps.shopify.com/shopify-forms (HTTP 200, Free)

14. Shopify Email (now Shopify Messaging)
- Hub: https://help.shopify.com/en/manual/promoting-marketing/create-marketing/shopify-messaging (CONFIRMED). The old .../promoting-marketing/shopify-email URLs redirect to the parent page, so do not use them.
- Pricing: https://help.shopify.com/en/manual/promoting-marketing/create-marketing/shopify-messaging/email/pricing (CONFIRMED)
  - 10,000 free emails per calendar month on Basic, Grow, Advanced and Plus. Unused emails do not roll over.
  - After that: USD 1 per 1,000 emails, then USD 0.65 per 1,000 after 300k, then USD 0.55 per 1,000 after 750k.
  - Abandoned checkout automations are always free.
- Consent: https://help.shopify.com/en/manual/promoting-marketing/create-marketing/customer-contact-information (CONFIRMED)
  - Checkout opt-in: Settings > Checkout > "Marketing opt-in".
  - Subscriber list: Customers > "Email subscribers" segment.
  - Double opt-in: Settings > Notifications > Customer notifications > Marketing double opt-in.
- App listing: https://apps.shopify.com/shopify-messaging (apps.shopify.com/shopify-email redirects here; HTTP 200)

15. Sitemap and Search Console: https://help.shopify.com/en/manual/promoting-marketing/seo/find-site-map (CONFIRMED)
- The sitemap is at https://yourdomain/sitemap.xml.
- Submit it in Search Console: Indexing > Sitemaps > enter "sitemap.xml" > SUBMIT.
- Verify the site: add a URL-prefix property and choose the "HTML tag" method. In Shopify, go to Online Store > theme "..." > Edit code > Layout/theme.liquid, paste the tag under <head>, Save, then click Verify in Search Console.
- A DNS TXT record (Domain property) also works.
- The store password (private mode) must be off for verification and crawling to work.

16. Dev docs
- App proxy: https://shopify.dev/docs/apps/build/online-store/app-proxies (CONFIRMED). Page title: "About app proxies and dynamic data".
  - Configure [app_proxy] in shopify.app.toml with url, prefix (a, apps, community or tools) and subpath.
  - Needs the write_app_proxy scope.
  - .../display-dynamic-data redirects here.
- Dev Dashboard: https://dev.shopify.com/dashboard/ (URL taken from the official doc; curl gets HTTP 406 because the page needs a login)
- Create-app doc: https://shopify.dev/docs/apps/build/dev-dashboard/create-apps-using-dev-dashboard (CONFIRMED). Steps: Apps > "Create app" > "Start from Dev Dashboard" > name > Create.

17. WhatsApp
- Native option: Shopify Messaging now sends WhatsApp marketing (changelog dated July 29, 2026: https://changelog.shopify.com/posts/shopify-messaging-now-supports-whatsapp-marketing).
  - Help page: https://help.shopify.com/en/manual/promoting-marketing/create-marketing/shopify-messaging/whatsapp (CONFIRMED that the page exists).
  - India eligibility and WhatsApp pricing: UNCONFIRMED. The pages read do not list countries or prices, and there is a separate requirements page I could not reach.
  - Needs a paid plan. Sends only to WhatsApp opt-in subscribers. A checkout WhatsApp checkbox is available.
- Third-party apps (App Store URLs checked HTTP 200; prices from the listings):
  - Interakt (Jio Haptik): https://apps.shopify.com/interakt-sales. Free plan or trial; paid tiers $41, $51 and $99/mo plus Meta conversation charges.
  - Wati: https://apps.shopify.com/wati-abandonedcart-recovery ("Wati: WA Cart Recovery & AI"). From $69/mo; also $149 and $349; free trial.
  - AiSensy: https://apps.shopify.com/aisensy-whatsapp-marketing. Free plan or trial. Reviews are mixed.
  - Gupshup: https://apps.shopify.com/gupshup-workflow-automation ("Gupshup: WhatsApp Marketing", free plan). Also https://apps.shopify.com/gupshup-notify.
  - MSG91 (extra option): https://apps.shopify.com/msg91
  - API approval: all four are WhatsApp Business Platform (API) providers. You onboard a number to the WhatsApp Business Platform through them, and each marketing template needs Meta approval. Their listings were not read in detail, so treat the exact onboarding steps as UNCONFIRMED.
- Opt-in rules:
  - WhatsApp Business Messaging Policy: https://business.whatsapp.com/policy. It redirects by locale to https://whatsappbusiness.com/policy/ (HTTP 200). Use ?lang=en for English.
  - Meta "Get opt-in for WhatsApp": https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in (HTTP 200). The opt-in must say clearly that the person agrees to WhatsApp messages from the named business and must follow applicable law. Opt-outs must be honoured.
  - The old developers.facebook.com/docs/whatsapp/overview/getting-opt-in URL is the previous version.
- Shopify Inbox: https://apps.shopify.com/inbox. It is chat only, not WhatsApp marketing.

## B. Meta (help page titles read from the HTML; locale=en_US)

18. Business portfolio: https://www.facebook.com/business/help/1710077379203657, "Create a business portfolio in Meta Business Suite" (CONFIRMED)

19. Instagram professional account: https://help.instagram.com/502981923235522, "Set up a professional Instagram account to access business or creator tools and controls" (CONFIRMED)
- Background article: https://help.instagram.com/138925576505882, "About professional accounts on Instagram".
- In-app path (from search snippets of the Help Center): Profile > menu > "Account type and tools" > "Switch to professional account" > choose a category > Business.

20. Events Manager and Test Events
- Events Manager: https://business.facebook.com/events_manager. This is the login-gated app; logged-out visitors are redirected to a login page.
- Test events: https://www.facebook.com/business/help/2040882565969969, "Test events tool: verify app and web browser events for Meta" (CONFIRMED from the page's H1)
- Pixel setup: https://www.facebook.com/business/help/952192354843755, "Set up and install the Meta Pixel"
- Conversions API: https://www.facebook.com/business/help/2041148702652965, "About Conversions API"

21. Audiences
- About custom audiences: https://www.facebook.com/business/help/744354708981227 (CONFIRMED)
- Website custom audience: https://www.facebook.com/business/help/1474662202748341, "Create a website custom audience" (CONFIRMED). Explainer: https://www.facebook.com/business/help/610516375684216, "Learn about website custom audiences".
- Lookalikes: https://www.facebook.com/business/help/164749007013531, "About lookalike audiences", and https://www.facebook.com/business/help/465262276878947, "Create a Lookalike Audience" (both CONFIRMED)
- Instagram engager (engagement) audience: I found no official article URL: UNCONFIRMED. In Ads Manager the flow is Audiences > Create audience > Custom audience > Meta sources: Instagram account. Retention can be up to 365 days per third-party guides; the exact limit is UNCONFIRMED.

22. Blueprint
- https://www.facebook.com/business/learn, "Meta Blueprint: Free online training for advertising on Facebook" (CONFIRMED)
- Course catalog: https://www.facebookblueprint.com/student/catalog (facebookblueprint.com redirects here; title "Meta Blueprint : Learn new skills ...")

23. Budget and Advantage+
- Official articles (titles CONFIRMED; the INR figures could not be read because the pages render with JavaScript):
  - https://www.facebook.com/business/help/203183363050448, "Best Practices for Minimum Budgets"
  - https://www.facebook.com/business/help/190490051321426, "About Daily Budgets"
  - https://www.facebook.com/business/help/214319341922580, "About budgets"
- India minimum: there is no official INR figure: UNCONFIRMED.
  - Meta sets minimums in USD and converts them. Third-party sources say about $1/day for impression delivery and about $5/day for clicks or conversions.
  - India blogs cite about ₹40/day as the floor for impression delivery.
  - Practical advice: ₹300-₹1,000/day per ad set for a small store.
  - Ads Manager shows the real minimum when you type a budget.
- Advantage+ naming: https://www.facebook.com/business/help/1362234537597370, "About Advantage+ Sales Campaigns" (CONFIRMED)
  - "Advantage+ shopping campaigns" were renamed "Advantage+ sales campaigns" in 2025. Per third-party sources, this is more than a rename (audience suggestions, exclusions, more ad sets). The API phased out the old type in Q1 2026.

## C. Google

24. GA4
- Setup: https://support.google.com/analytics/answer/9304153, "Set up Analytics for a website and/or app" (CONFIRMED)
  - Admin > Create > Account, then Property.
  - Then Data collection and modification > Data streams > Add stream > Web, and copy the Measurement ID (G-...).
- Traffic acquisition: https://support.google.com/analytics/answer/12923437, "[GA4] Traffic acquisition report" (CONFIRMED)
  - Path: Reports > Acquisition > Traffic acquisition.
  - Dimensions: Session source/medium and Session campaign (switch the primary dimension or add a secondary one).
- Campaigns and traffic sources: https://support.google.com/analytics/answer/11242841 (CONFIRMED)

25. Search Console
- Add a property: https://support.google.com/webmasters/answer/34592, "Add a website or platform property to Search Console" (CONFIRMED)
- Verify: https://support.google.com/webmasters/answer/9008080, "Verify your site ownership" (CONFIRMED)
- Sitemaps: https://support.google.com/webmasters/answer/7451001, "Sitemaps report" (CONFIRMED)
- Tool: https://search.google.com/search-console (logged-out visitors go to /about)

26. Skillshop: https://skillshop.withgoogle.com/ (CONFIRMED)

27. Campaign URL Builder: https://ga-dev-tools.google/ga4/campaign-url-builder/ (GA4 version, HTTP 200). https://ga-dev-tools.google/campaign-url-builder/ also returns 200; its title is "Campaign URL Builder". (CONFIRMED)

## D. AI video and image tools (status as of 2026-10-10; flag the uncertain items)

OpenAI Sora: DISCONTINUED. Do not recommend it.
- Several sources (the-decoder, others) report that the consumer Sora app and web closed on April 26, 2026, and the Sora API on September 24, 2026.
- openai.com/index/sora-2 returned 403 to my fetch. Search snippets show it carries the notice "As of April 26, 2026, the Sora product is no longer available."
- The Sora app never officially launched in India.
- Status: CONFIRMED by multiple sources; I could not read the official page directly.

ChatGPT image generation (ChatGPT Images 2.0, model gpt-image-2, launched about April 21, 2026)
- URL: https://chatgpt.com (403 to curl, which is normal bot-blocking)
- Works in India.
- Prices from third-party sources: ChatGPT Go about ₹399/mo (the free India promotion appears to have ended January 2026); Plus about ₹1,999/mo. Exact current prices: UNCONFIRMED.
- Consistency: upload a reference image. Thinking mode (paid plans) can make up to 8 images that keep the same character.

Google Veo / Flow / Gemini
- Flow: https://labs.google/flow now redirects to https://flow.google.com/ (title "Google Flow - AI Creative Studio for Video, Images & Custom Tools") (CONFIRMED)
- Gemini app: https://gemini.google.com
- India plans, read from the official page https://gemini.google/in/subscriptions/?hl=en-IN (CONFIRMED):
  - Google AI Plus ₹399/mo: 200 Flow credits
  - Google AI Pro ₹1,950/mo: 1,000 Flow credits, plus a "limited trial of Veo 3.1 Lite"
  - Google AI Ultra from ₹6,500/mo (₹19,500 tier): 10k or 25k credits
- All plans list "access to Gemini Omni Flash", which looks like Google's newer 2026 video model. Treat the Veo naming as in flux.
- Jio offers reportedly include free AI Pro for eligible users: UNCONFIRMED.
- Consistency: "Ingredients to video" lets you give up to 3 reference images for characters or products. This comes from third-party sources; I could not confirm whether it is still the name in the 2026 Flow UI.

Kling AI
- https://kling.ai (klingai.com and app.klingai.com redirect here) (CONFIRMED). The homepage now lists Kling 4.0 video and Kling Image 3.0.
- Works in India (it is a web app; no block known).
- Price (third-party): Standard about $7-10/mo, Pro about $24-37, Premier about $60-92. Official pricing: UNCONFIRMED.
- Consistency: "Elements" / multi-image reference and multi-shot (up to 6 shots on 3.0). This is from third-party sources; I could not confirm the feature names on the homepage.

Runway
- https://runway.com (runwayml.com redirects here). Pricing: https://runway.com/pricing (CONFIRMED)
- Free: 125 credits one-time
- Standard: $15/mo ($12/mo billed annually), 625 credits
- Pro: $35/mo ($28/mo billed annually), 2,250 credits
- Max: $95/mo ($76/mo billed annually), 9,500 credits
- Models: Gen-4.5, Gen-4, Aleph 2.0, and third-party Kling 3.0, Seedance and Nano Banana Pro.
- Consistency: Gen-4 "References" (up to 3 reference images), per third-party sources. The pricing page does not mention References.
- Works in India.

Hailuo (MiniMax)
- https://hailuoai.video (HTTP 200) (CONFIRMED that the site loads)
- Price from third-party sources: about $9.99 Standard and $34.99 Pro on the US App Store: UNCONFIRMED.
- Model: Hailuo 02/2.3, with "Hailuo 3/H3" reportedly launched July 31, 2026: UNCONFIRMED.
- Consistency: subject reference: UNCONFIRMED.

CapCut: STILL BLOCKED IN INDIA (CONFIRMED)
- capcut.com returns HTTP 451 from this India-located machine.
- Multiple sources say that as of October 8, 2026 it is not in the Indian Play Store or App Store. It has been blocked since 2020 under IT Act Section 69A.
- Do not recommend it, and do not suggest workarounds.

India-safe editors
- Instagram Edits (Meta): https://edits.instagram.com (HTTP 200). Free; needs an Instagram account; mobile only; captions, teleprompter, direct Reels publishing.
- InShot: https://inshot.com (HTTP 200). Free with watermark. Pro is about ₹399/mo per a third-party tracker: UNCONFIRMED.
- VN Video Editor: https://www.vlognow.me (HTTP 200). Free, no watermark; some paid assets.
- Canva video editor: https://www.canva.com/video-editor/ (403 to curl, which is normal bot-blocking). Free tier. Canva Pro India price is UNCONFIRMED: reports range from ₹499/mo to about ₹3,999-4,500/yr; check canva.com/en_in/pricing.
