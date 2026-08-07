/* ---------------- UPDATED GRAMMAR PRACTICE FETCH LOGIC ---------------- */

async function updateGrammarTopicDropdown() {
  grammarTopicSelect.innerHTML = '';
  
  const allOpt = document.createElement('option');
  allOpt.value = "ALL";
  allOpt.textContent = "All Grammar Topics";
  grammarTopicSelect.appendChild(allOpt);

  try {
    const response = await fetch(`/api/grammar/topics?unit=${encodeURIComponent(currentUnit)}`);
    const data = await response.json();

    if (data.topics) {
      data.topics.forEach(topicName => {
        const opt = document.createElement('option');
        opt.value = topicName;
        opt.textContent = topicName;
        grammarTopicSelect.appendChild(opt);
      });
    }
  } catch (err) {
    console.error("Error loading grammar topics:", err);
  }

  grammarTopicSelect.value = "ALL";
  currentGrammarTopic = "ALL";
}

async function newGrammarExercise() {
  try {
    const url = `/api/grammar/exercise?unit=${encodeURIComponent(currentUnit)}&topic=${encodeURIComponent(currentGrammarTopic)}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      grammarEnEl.textContent = "No sentences available for this topic.";
      grammarBank.innerHTML = '';
      grammarAnswer.innerHTML = '';
      return;
    }

    grammarEx = await response.json();

    grammarSlotIndex = 0;
    grammarMistakesThisRound = 0;
    grammarComplete.textContent = '';
    grammarNextBtn.style.display = 'none';
    grammarRevealBtn.style.display = 'inline-block';
    grammarSkipBtn.style.display = 'inline-block';

    grammarTopicTag.textContent = currentGrammarTopic === "ALL" ? "GRAMMAR PRACTICE · ALL TOPICS" : currentGrammarTopic;
    grammarEnEl.textContent = grammarEx.en;

    grammarAnswer.innerHTML = '';
    const ph = document.createElement('span');
    ph.className = 'placeholder';
    ph.textContent = 'tap words & particles below, in order →';
    grammarAnswer.appendChild(ph);

    let items = [];
    grammarEx.slots.forEach((opts, si) => {
      opts.forEach(o => items.push({ t: o.t, ok: o.ok, isParticle: o.isParticle, si }));
    });
    items = shuffled(items);

    grammarBank.innerHTML = '';
    items.forEach(it => {
      const chip = document.createElement('div');
      chip.className = 'chip' + (it.isParticle ? ' particle-chip' : '');
      chip.textContent = it.t;
      chip.dataset.si = it.si;
      chip.addEventListener('click', () => onGrammarChipClick(it, chip));
      grammarBank.appendChild(chip);
    });
  } catch (err) {
    console.error("Failed to load exercise from API:", err);
  }
}