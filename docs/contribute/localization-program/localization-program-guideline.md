# Localization Program Guideline

In the process of **letting TON become the most successful Blockchain**, how to let TON docs be more understandable to people around the world is also an important issue to resolve, that's why we need localization, and we're **glad** you're here ready to participate in.

<br />

:::tip TON X TownSquare localization program
This system **TON X TownSquare localization program** was designed by :            
[**TownSquare**](https://github.com/TownSquareXYZ) one of the closest partners of **TON**. 

We commit ourselves to making an open infrastructure for multilingual community collaboration to **make TON get into a better phrase**, which includes:
  1. **Suitable for multilingual communities**
  2. **Automate development, integration, and deployment**
  3. **Decoupling the roles of developer, translator, and verifier**
  4. **Community contribution incentive**
    
    **...**

It's not just some project for only one language user, our goal is **for the global developer ecosystem**.
:::

## How to add support for a new language
For now, we have all languages we wanted in Crowdin, if you are a community manager, you just need:
1. Add a new branch named your `[lang]_localization`(like if you're korean community manager use `ko_localization`), on [TownSquareXYZ/ton-docs](https://github.com/TownSquareXYZ/ton-docs).
2. **Contact vercel owner of this repo**, let him know what language you wanna show in menu.
3. create a pr request to dev branch. **Never merge it to dev**, it just for preview.

That's all! now you can see the preview of your language in the pr request. 
![ko preview](/img/localizationProgramGuideline/ko_preview.png)

When your lang is ready to show on TON docs, create an issue, we'll set your lang into prod env.



## Roles

Here are the **roles** you can be in the system :

- **Proofreader**
- **Translator** ( in-house or community )

Next, we'll have some specific guides about roles you wanna get into.

Our localization project is running on [Crowdin](https://crowdin.com/project/ton-docs).

:::info IMPORTANT

Before you start contributing, **read the guidelines below**! They will help you ensure the level of standardization and quality that will make the review process much faster.

## side-by-side mode

All these works are based on **side-by-side** mode in Crowdin Editor, if you don't know how to get into this, click a file you wanna start work, on the top right of the page, you can see Editor view button, we choose **side-by-side** mode, which will make editor more clear. 
![side-by-side mode](/img/localizationProgramGuideline/side-by-side.png)
:::

### Proofreader

As a **Proofreader**, the files that have a **blue progress bar** are you gonna work in.
![proofread step1](/img/localizationProgramGuideline/proofread-step1.png)
Click one of the files, you'll get into an editing interface.

#### Let's start contribute.

1. First of all, we should make your workspace more suitable for work:

  Make sure you're in [**side by side mode**](#side-by-side-mode), then let's find out which lines of translations need to be proofread, you can see there is a **filter** button on the **right** of Search in file input, let's choose **Not Approved** option.
![proofread filter](/img/localizationProgramGuideline/proofread-filter.png)


2. Great, we're ready to start work now, here are the rules you should follow:
   - select a string that has a **blue cube icon** on left, which means it's translated but hasn't been proofread, check it carefully:
     - if it's all **right**, click the ☑️ button on top.
     - if it's **not right**, just ignore it, go to the next line.

![proofread approved](/img/localizationProgramGuideline/proofread-approved.png)
     

:::info
**You also have the right to check lines which already been proofread**: 
  1. set a filter option to **Approved**. 
  2. if there is an approved line that still has issues, you can **click the same ☑️ button** on top, to set this line's state back to need proofreading.
:::

<br/>

3. Well done! if you wanna go to the next file in editor mode, just **click the file name** on the top, you can see a pop-up window, click the file name you will be transported to that file, and continue your proofread travel.
![to next](/img/localizationProgramGuideline/redirect-to-next.png)

#### We also provide you with a great function: 
You can **see the fruits of your labor in time**. Every content approved by proofreaders will be deployed in a preview website in one hour. Check [**our repo**](https://github.com/TownSquareXYZ/ton-docs/pulls), you'll find **preview** link in newest pr.
![preview link](/img/localizationProgramGuideline/preview-link.png)


### Translator

The **translator** decides what readers can see in this doc, so make sure to translate docs faithfulness and expressiveness, in another way, **make your translation close to the original meaning and also as simple and understandable as possible**.

Our mission is to make the **blue progress bar** of the file reach 100%.

#### Let's start translate.

Don't be stressed about this, you can ask for help from **AI** and **other translators**, follow these guides to help you do better:

Click files that haven't been 100% translated.
![translator select](/img/localizationProgramGuideline/translator-select.png)

Again, after you get into the editor, make sure you're in [**side by side mode**](#side-by-side-mode):

1. To list lines that need to be translated. you can see there is a **filter** button on the right of Search in file input, let's choose **Untranslated**.
![translator filter](/img/localizationProgramGuideline/translator-filter.png)

2. You can see the whole page has been separated to four-part:
    - The **top left** one is where you **input your translation**. According to Source string, you should input the correct translation to its right input.
    - The **bottom left** one is the preview of the translated file. Make sure to **keep the translated format** as same as the original one, this is also **important**.
    - The **bottom right** one are the **suggestion translations** from crowdin. If there is a right translation in there, you can just click that translate, and crowdin will input that into the target translation. 

      :::info
        it's convenient, but be aware, they are **not always right**, so be careful when you use this function, especially when the Source string include a link or some other path, **don't let suggest translations change the links**.
      :::

  
3. Once you think your translation is done or wanna take a break, **click Save button** on the top, your current translation will update to the project, waiting for proofreading.
![translator save](/img/localizationProgramGuideline/translator-save.png)


4. Congrats, now you know how to work like a translator, if you wanna go to the next file in the editor, just **click the file name** on the top, and it will have a pop-up window, click the file name you will be transported to that file, enjoy it!
![to next](/img/localizationProgramGuideline/redirect-to-next.png)