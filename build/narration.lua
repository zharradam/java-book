-- Turns the book into a narration script for VoiceStudio's Audiobook screen.
--
-- Run after extracts.lua (without build/metadata.yaml, so extracts keep their
-- italics): every "# Title" is a chapter; quoted extracts are wrapped in
-- [voice:Quote] ... [voice:] so they are read in a second voice, while
-- Stephen's own comments inside an extract stay with the narrator. Pictures,
-- captions, credit lines, tables and web addresses are left out.
-- The words themselves are copied verbatim, as in the EPUB.

local OPEN, CLOSE = '[voice:Quote]', '[voice:]'

local function is_url(el)
  return (el.t == 'Link' or el.t == 'Str') and pandoc.utils.stringify(el):match('^https?:') ~= nil
end

local function words(s)
  local n = 0
  for _ in s:gmatch('%w+') do n = n + 1 end
  return n
end

-- inlines -> list of {text, quote}; quote is nil for spaces and punctuation,
-- which never switch voice on their own
local function runs(inlines, quote, out)
  for _, el in ipairs(inlines) do
    if el.t == 'Image' or is_url(el) then
    elseif el.t == 'Emph' then runs(el.content, true, out)
    elseif el.t == 'Quoted' then
      local q = el.quotetype == 'DoubleQuote' and { '“', '”' } or { '‘', '’' }
      table.insert(out, { q[1] }); runs(el.content, quote, out); table.insert(out, { q[2] })
    elseif el.t == 'Space' or el.t == 'SoftBreak' or el.t == 'LineBreak' then
      table.insert(out, { ' ' })
    elseif el.content then runs(el.content, quote, out)
    else
      local s = pandoc.utils.stringify(el)
      local q = nil
      if words(s) > 0 then q = quote end
      table.insert(out, { s, q })
    end
  end
  return out
end

-- Spoken forms for things a voice would misread: scanning errors, period
-- notation, editorial marks. Applies to the narration script only; the book's
-- text is untouched.
local MONTHS = { 'January', 'February', 'March', 'April', 'May', 'June', 'July',
                 'August', 'September', 'October', 'November', 'December' }
local function date(d, m, y)
  local name = MONTHS[tonumber(m)]
  return name and (tonumber(d) .. ' ' .. name .. ' ' .. y) or nil
end
local KEEP = { MRCS = true, FS = true, SA = true, UK = true, RN = true }
local function titlecase(w) return w:sub(1, 1) .. w:sub(2):lower() end

local SPEECH = {
  -- scanning errors the book's readers silently correct
  { '1/21b', 'half a pound' }, { '101/2 to 11', '10 and a half to 11' }, { ' l oz%.', ' 1 ounce' },
  { '1/2 oz', 'half an ounce' }, { '1 1/2 days', 'a day and a half' }, { '1/4 before 8', 'a quarter before 8' },
  { '(%d+)/(%d)(18%d%d)', date },                      -- 16/61842 = 16/6/1842
  { 'Graham%[Gahan}', 'Graham (Gahan)' },
  -- dates written d/m/yyyy, and ranges of them
  { '(%d+)/(%d+)/(1[78]%d%d)%-', function (d, m, y) local s = date(d, m, y); return s and s .. ' to ' end },
  { '(%d+)/(%d+)/(1[789]%d%d)', date },
  -- money: GBP is a scanning error for the pound sign; n/- is shillings
  { 'GBP ?(%d+)%.(%d+)s', '%1 pounds %2 shillings' }, { 'GBP ?(%d+)', '%1 pounds' }, { '(%d+)/%-', '%1 shillings' },
  -- positions and temperatures: 39 o 22' South lat.
  { "(%d+) ?o ?(%d+) ?'", '%1 degrees %2 minutes ' }, { '(%d+) ?o ?(%d+) ?’', '%1 degrees %2 minutes ' },
  { '(%d+) ?o ?([%.%s])', '%1 degrees%2' }, { 'minutes  ', 'minutes ' },
  -- only after a compass point, so "the late Colin Kerr" and "a long voyage" are left alone
  { '([Ss]outh) lat%.?', '%1 latitude' }, { 'North lat%.?', 'North latitude' }, { ' S%. lat', ' South latitude' },
  { '(East) long%.?', '%1 longitude' }, { '(West) long%.?', '%1 longitude' }, { 'E%. long', 'East longitude' },
  { 'Therm%.', 'Thermometer' }, { 'FS%. lat%.', 'F S latitude' },
  -- times and abbreviations
  { '(%d)a%.m%.%.', '%1 a.m.' }, { '(%d)pm', '%1 p.m.' }, { '(%d):(%d%d)am', '%1:%2 a.m.' },
  { 'gentn%.', 'gentleman' }, { 'Gentn', 'gentleman' }, { 'No%.? (%d)', 'Number %1' }, { '& Co%.?', 'and Company' },
  -- editorial marks
  { ' ?%(sic%)', '' }, { '%-Ed%.', 'Editor.' },
  -- stray hyphens left by the scan: "great -granddaughter", "grown- up"
  { '([A-Za-z]) %-([A-Za-z])', '%1-%2' }, { '([A-Za-z])%- ([a-z])', '%1-%2' }, { '([A-Za-z])%- ([A-Z])', '%1, %2' }, { '(%d)%- ([A-Z])', '%1 to %2' },
  { ' %.', '.' },
}

local function spoken(s)
  -- keep the voice tags out of reach of the rules below
  s = s:gsub('%[voice:Quote%]', '\1'):gsub('%[voice:%]', '\2')
  for _, r in ipairs(SPEECH) do s = s:gsub(r[1], r[2]) end
  s = s:gsub('%[', '('):gsub('%]', ')')                -- editorial brackets read as an aside
  -- words in capitals are read as words, not spelt out (initialisms excepted)
  s = s:gsub('()([A-Z][A-Z]+)()', function (i, w, j)
    if KEEP[w] or s:sub(i - 1, i - 1):match('[A-Za-z]') or s:sub(j, j):match('[a-z]') then return w end
    return titlecase(w)
  end)
  return (s:gsub('\1', OPEN):gsub('\2', CLOSE))
end

-- the text of one paragraph; in_extract = italic is quotation, roman is Stephen
local function speak(inlines, in_extract)
  local parts, voice = {}, false
  for _, r in ipairs(runs(inlines, false, {})) do
    local q = in_extract and r[2]
    if q ~= nil and q ~= voice then
      table.insert(parts, q and OPEN or CLOSE)
      voice = q
    end
    table.insert(parts, r[1])
  end
  if voice then table.insert(parts, CLOSE) end
  -- pandoc puts a no-break space after "Mr." and the like; a plain one reads the same
  return spoken((table.concat(parts):gsub('\194\160', ' '):gsub('%s+', ' '):gsub('^ ', ''):gsub(' $', '')
    :gsub('%[voice:Quote%] ', ' ' .. OPEN):gsub(' %[voice:%]', CLOSE .. ' ')))
end

local function para(text) return pandoc.Para({ pandoc.Str(text) }) end

local function blocks(list, in_extract, out)
  for _, b in ipairs(list) do
    if b.t == 'Header' then
      local title = spoken(pandoc.utils.stringify(b.content):gsub('94p', ' '))
      out:insert(para(b.level == 1 and '# ' .. title or title))
    elseif b.t == 'Para' or b.t == 'Plain' then
      local has_url = false
      b.content:walk({ Inline = function(l) if is_url(l) then has_url = true end end })
      local text = speak(b.content, in_extract)
      -- a paragraph that is only a web address ("Found at <http://…>") is a citation
      if words(text:gsub('%[voice:%a*%]', '')) > (has_url and 3 or 0) then out:insert(para(text)) end
    elseif b.t == 'BlockQuote' then blocks(b.content, true, out)
    elseif b.t == 'Div' then blocks(b.content, in_extract, out)
    elseif b.t == 'LineBlock' then
      for _, line in ipairs(b.content) do out:insert(para(speak(line, in_extract))) end
    end
    -- Figure, Table, lists, rules and raw blocks are not read aloud
  end
  return out
end

function Pandoc(doc)
  return pandoc.Pandoc(blocks(doc.blocks, false, pandoc.List()))
end
