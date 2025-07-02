import express from 'express';
import OpenAI from 'openai';

const app = express();
app.use(express.json({ limit: '10mb' }));

const SYSTEM_PROMPT = 'Tum ek madadgar Hinglish assistant ho. Jawab hamesha 80 words se kam rakho, halka sa friendly tone aur thode fillers jaise "uh" use karo.';

app.post('/llm', async (req, res) => {
  try {
    const { messages } = req.body;
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        ...messages.slice(-20)
      ]
    });
    res.json(response.choices[0].message);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'llm_error' });
  }
});

const port = process.env.PORT || 4000;
app.listen(port, () => console.log(`llm service on ${port}`));
