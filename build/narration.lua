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
  return table.concat(parts):gsub('\194\160', ' '):gsub('%s+', ' '):gsub('^ ', ''):gsub(' $', '')
    :gsub('%[voice:Quote%] ', ' ' .. OPEN):gsub(' %[voice:%]', CLOSE .. ' ')
end

local function para(text) return pandoc.Para({ pandoc.Str(text) }) end

local function blocks(list, in_extract, out)
  for _, b in ipairs(list) do
    if b.t == 'Header' then
      local title = pandoc.utils.stringify(b.content)
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
