-- Sets quoted extracts (diaries, letters, newspapers) apart from the narrative.
--
-- A paragraph that is italic throughout - optionally led by a bold date - is an
-- extract: it becomes an indented block quotation, and runs of them are merged.
-- A paragraph marked ">" in the manuscript is an extract that Stephen interrupts
-- with a comment of his own.
--
-- With `extracts_upright: true` in build/metadata.yaml the extracts are set
-- upright, and any comment inside one is set in italic, so that the two voices
-- stay distinct. Set it to false to keep extracts italic.
local upright = false

local CURLY = { '\226\128\156', '\226\128\157', '\226\128\152', '\226\128\153' }

local function only_punct(s)
  for _, q in ipairs(CURLY) do s = s:gsub(q, '') end
  return s:match('^[%p%s]*$') ~= nil
end

local function extract_like(inlines)
  local emph = false
  for _, el in ipairs(inlines) do
    if el.t == 'Emph' then emph = true
    elseif el.t == 'Strong' or el.t == 'Space' or el.t == 'SoftBreak' or el.t == 'LineBreak' then
    elseif el.t == 'Str' and only_punct(el.text) then
    elseif el.t == 'Quoted' then
      if extract_like(el.content) then emph = true else return false end
    else return false end
  end
  return emph
end

local function unwrap(inlines)
  return inlines:walk({ Emph = function(e) return e.content end })
end

-- inside a marked extract: italic -> upright, and Stephen's roman -> italic
local function invert(inlines)
  local out, run = pandoc.List(), pandoc.List()
  local function flush()
    local words = false
    for _, el in ipairs(run) do
      if el.t ~= 'Str' or not only_punct(el.text) then
        if el.t ~= 'Space' and el.t ~= 'SoftBreak' then words = true end
      end
    end
    if words then
      while #run > 0 and (run[1].t == 'Space' or run[1].t == 'SoftBreak') do out:insert(run:remove(1)) end
      local tail = pandoc.List()
      while #run > 0 and (run[#run].t == 'Space' or run[#run].t == 'SoftBreak') do tail:insert(1, run:remove(#run)) end
      out:insert(pandoc.Emph(run)); out:extend(tail)
    else
      out:extend(run)
    end
    run = pandoc.List()
  end
  for _, el in ipairs(inlines) do
    if el.t == 'Emph' then flush(); out:extend(el.content)
    elseif el.t == 'Strong' then flush(); out:insert(el)
    elseif el.t == 'Quoted' then flush(); el.content = invert(el.content); out:insert(el)
    else run:insert(el) end
  end
  flush()
  return out
end

-- A paragraph that opens "37." is read by Typst as a numbered-list item, which
-- takes the first line and strands the rest as a separate paragraph. Escape the
-- full stop so the paragraph stays a paragraph. (PDF only; the EPUB is unaffected.)
local function keep_as_paragraph(p)
  if not FORMAT:match('typst') then return nil end
  local first = p.content[1]
  if first and first.t == 'Str' then
    local num, rest = first.text:match('^(%d+)%.(.*)$')
    if num then
      p.content[1] = pandoc.RawInline('typst', num .. '\\.')
      if rest ~= '' then p.content:insert(2, pandoc.Str(rest)) end
      return p
    end
  end
  return nil
end

return {
  { Meta = function(m) if m.extracts_upright then upright = true end end },
  { BlockQuote = function(q)
      if not upright then return nil end
      return q:walk({ Para = function(p) return pandoc.Para(invert(p.content)) end })
    end },
  { Blocks = function(blocks)
      local out, run = pandoc.List(), pandoc.List()
      local function flush()
        if #run > 0 then out:insert(pandoc.BlockQuote(run)); run = pandoc.List() end
      end
      for _, b in ipairs(blocks) do
        if b.t == 'Para' and extract_like(b.content) then
          if upright then b = pandoc.Para(unwrap(b.content)) end
          run:insert(b)
        elseif b.t == 'BlockQuote' and #run > 0 then
          run:extend(b.content)          -- a marked extract continues the run
        else
          flush(); out:insert(b)
        end
      end
      flush()
      return out
    end },
  { Para = keep_as_paragraph },
}
