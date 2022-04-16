# Inclusivity app

An app to determine whether blocks of text may be offensive or un-inclusive e.g. racist, sexist or transphobic.

The app allows users to paste in text blocks of up to roughly 1,500 words, select a number of dimensions over which to scan the words for offensive material, and then for each dimension the model returns a score for how offensive the text is and an explanation of it's score.

The app is currently a prototype intended o determine the potential utility of a larger scale up that could be used e.g. by companies to scan their text outputs to ensure they are not publishing offesnive material. The app could asl be used by people to scan news sites they are interested in to uncover latent biases in their reporting of which they were unaware.

### Backend {#backend}

The backend of the app is powered by the Davinci GPT3 model. The app connects to theis model using the open GPT3 API.
