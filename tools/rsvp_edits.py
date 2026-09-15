# -*- coding: utf-8 -*-
"""RSVP / guest-policy edits requested 2026-09-15. Imported by build_page.py."""
import re
BS = chr(92)
NL = chr(10)


def apply(out):
    R = []
    # --- dinner description (details section) ---
    R.append((re.compile(r'<p class="t" data-es>\s*Entrada, plato fuerte y torta de matrimonio\..*?</p>', re.S),
              '<p class="t" data-es>\n        Te serviremos un elegante aperitivo, una cena deliciosa y llena de sabor, y torta de matrimonio.\n      </p>'))
    R.append((re.compile(r'<p class="t" data-en>\s*An appetizer, a main course and wedding cake\..*?</p>', re.S),
              '<p class="t" data-en>\n        You will be served an elegant appetizer, a delicious and flavorful dinner, and wedding cake.\n      </p>'))
    # --- reception: adults only note ---
    R.append(('<p class="t">Calle 73 # 8-60 · Zona G, Bogotá D.C.</p>',
              '<p class="t">Calle 73 # 8-60 · Zona G, Bogotá D.C.</p>\n      <p class="t" data-es>Recepción solo para adultos (mayores de 18).</p>\n      <p class="t" data-en>The reception is adults only (18+).</p>'))
    # --- FAQ children ---
    R.append(('<p data-es>La ceremonia es para todos. La cena y el baile son solo para adultos.</p>',
              '<p data-es>Los niños son bienvenidos en la ceremonia en la iglesia. Por favor no los lleves a la recepción: la cena y el baile son solo para adultos.</p>'))
    R.append(('<p data-en>The ceremony is for everyone. Dinner and dancing are adults only.</p>',
              '<p data-en>Children are welcome at the ceremony in the church. Please do not bring them to the reception: dinner and dancing are adults only.</p>'))
    # --- attendance: ceremony + reception ---
    R.append((re.compile(r'<span class="legend" data-es>¿Nos acompañas\?</span>.*?</div>\n      </fieldset>', re.S),
'''<span class="legend" data-es>¿Nos acompañas? · Ceremonia y recepción</span>
        <span class="legend" data-en>Will you join us? · Ceremony and reception</span>
        <div class="opts">
          <label class="opt"><input type="radio" name="asiste" value="ambos" checked>
            <span data-es>¡Sí, a la ceremonia y la recepción!</span><span data-en>Yes, ceremony and reception!</span></label>
          <label class="opt"><input type="radio" name="asiste" value="ceremonia">
            <span data-es>Solo a la ceremonia</span><span data-en>Ceremony only</span></label>
          <label class="opt"><input type="radio" name="asiste" value="no">
            <span data-es>No podré ir</span><span data-en>I can't make it</span></label>
        </div>
      </fieldset>'''))
    # --- companion: max +1, adults only, reception & dinner only ---
    R.append((re.compile(r'<span class="legend" data-es>Acompañantes</span>.*?</div>\n      </fieldset>', re.S),
'''<span class="legend" data-es>Acompañante · solo recepción y cena</span>
        <span class="legend" data-en>Plus one · reception and dinner only</span>
        <div class="opts">
          <label class="opt"><input type="radio" name="acomp" value="0" checked>
            <span data-es>Voy sin acompañante</span><span data-en>Just me</span></label>
          <label class="opt"><input type="radio" name="acomp" value="1">
            <span data-es>Con un acompañante (+1)</span><span data-en>With a plus one (+1)</span></label>
        </div>
        <p class="menu-note" data-es>Máximo un acompañante, mayor de 18 años. Los niños son bienvenidos únicamente en la ceremonia.</p>
        <p class="menu-note" data-en>One companion at most, 18 or older. Children are welcome at the ceremony only.</p>
      </fieldset>'''))
    # --- menu: description only, no selector ---
    R.append((re.compile(r'<fieldset class="field" id="grp-menu">.*?</fieldset>', re.S),
'''<div class="field" id="grp-menu">
        <span class="legend" data-es>Menú</span>
        <span class="legend" data-en>Menu</span>
        <p class="menu-note" data-es>Te serviremos un elegante aperitivo, una cena deliciosa y llena de sabor, y torta de matrimonio.</p>
        <p class="menu-note" data-en>You will be served an elegant appetizer, a delicious and flavorful dinner, and wedding cake.</p>
      </div>'''))
    # --- script: attendance states ---
    R.append(('''  function attending(){
    return form.querySelector('input[name=asiste]:checked').value === 'si';
  }
  function sync(){
    var on = attending();
    groups.forEach(function(id){ document.getElementById(id).style.display = on ? '' : 'none'; });
  }''',
'''  function attending(){
    return form.querySelector('input[name=asiste]:checked').value;
  }
  function sync(){
    var on = attending() === 'ambos';   /* companion, menu, diet and hotel apply to the reception only */
    groups.forEach(function(id){ document.getElementById(id).style.display = on ? '' : 'none'; });
  }'''))
    R.append(('''    if(attending()){
      lines.push(en ? 'Attending: yes' : 'Asisto: sí');
      lines.push((en ? 'Guests: ' : 'Acompañantes: ') + form.querySelector('input[name=acomp]:checked').value);
      lines.push((en ? 'Menu: ' : 'Menú: ') + form.querySelector('input[name=menu]:checked').value);
      var dieta''',
'''    var a = attending();
    if(a === 'ambos'){
      lines.push(en ? 'Attending: ceremony and reception' : 'Asisto: ceremonia y recepción');
      var plus = form.querySelector('input[name=acomp]:checked').value === '1';
      lines.push(en ? ('Plus one: ' + (plus ? 'yes (1 adult)' : 'no')) : ('Acompañante: ' + (plus ? 'sí (1 adulto)' : 'no')));
      var dieta'''))
    R.append(('''    }else{
      lines.push(en ? 'Attending: sorry, I cannot make it' : 'Asisto: lamentablemente no podré ir');
    }''',
'''    }else if(a === 'ceremonia'){
      lines.push(en ? 'Attending: ceremony only' : 'Asisto: solo a la ceremonia');
    }else{
      lines.push(en ? 'Attending: sorry, I cannot make it' : 'Asisto: lamentablemente no podré ir');
    }'''))
    # --- contact: real WhatsApp number + email fallback (2026-09-15) ---
    R.append(('var RSVP_WHATSAPP = "57XXXXXXXXXX";',
              'var RSVP_WHATSAPP = "18017066256";\nvar RSVP_EMAIL = "johanacastellanos11@gmail.com";'))
    R.append(('<p class="formnote" data-es>Al enviar se abrirá WhatsApp con tu respuesta lista para mandar.</p>',
              '<p class="formnote" data-es>Al enviar se abrirá WhatsApp (+1 801 706 6256) con tu respuesta lista para mandar. Si prefieres, escríbenos a <a class="maplink" href="mailto:johanacastellanos11@gmail.com">johanacastellanos11@gmail.com</a>.</p>'))
    R.append(('<p class="formnote" data-en>Sending opens WhatsApp with your response ready to go.</p>',
              '<p class="formnote" data-en>Sending opens WhatsApp (+1 801 706 6256) with your response ready to go. If you prefer, email us at <a class="maplink" href="mailto:johanacastellanos11@gmail.com">johanacastellanos11@gmail.com</a>.</p>'))
    R.append(('      <a class="btn btn-ghost" href="https://calendar.google.com/calendar/render?action=TEMPLATE',
              '      <button type="button" class="btn btn-ghost" id="rsvp-email">\n        <span data-es>Enviar por correo</span><span data-en>Send by email</span>\n      </button>\n      <a class="btn btn-ghost" href="https://calendar.google.com/calendar/render?action=TEMPLATE'))
    R.append(("  form.addEventListener('submit', function(e){\n    e.preventDefault();\n    var en = document.documentElement.lang === 'en';",
              "  function compose(){\n    var en = document.documentElement.lang === 'en';"))
    # the page script joins lines with a literal backslash-n; build that token without escaping headaches
    JOIN = "lines.join('" + BS + "n')"
    OLD_OPEN = ("    window.open('https://wa.me/' + RSVP_WHATSAPP + '?text=' + encodeURIComponent(" + JOIN + "), '_blank', 'noopener');" + NL + "  });")
    NEW_OPEN = NL.join([
        "    return { en: en, text: " + JOIN + " };",
        "  }",
        "  form.addEventListener('submit', function(e){",
        "    e.preventDefault();",
        "    var m = compose(); if(!m) return;",
        "    window.open('https://wa.me/' + RSVP_WHATSAPP + '?text=' + encodeURIComponent(m.text), '_blank', 'noopener');",
        "  });",
        "  document.getElementById('rsvp-email').addEventListener('click', function(){",
        "    var m = compose(); if(!m) return;",
        "    var subject = m.en ? 'RSVP — Tad & Johana' : 'Confirmación — Tad y Johana';",
        "    window.location.href = 'mailto:' + RSVP_EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(m.text);",
        "  });"])
    R.append((OLD_OPEN, NEW_OPEN))
    # --- regalo en sobre (after Hospedaje), humble and grateful ---
    GIFT = """    <div class="detail">
      <h3 data-es>Regalo en sobre</h3>
      <h3 data-en>Gift envelope</h3>
      <p class="t" data-es>
        Tu presencia es el regalo más grande que podemos recibir. Si además quieres tener un detalle
        con nosotros, siguiendo la tradición, un sobre será recibido con mucho cariño: habrá un lugar
        especial en la recepción para dejarlo. Gracias, de corazón.
      </p>
      <p class="t" data-en>
        Your presence is the greatest gift we could ask for. If you would also like to give us something,
        following Colombian tradition, an envelope will be received with love: there will be a special
        place at the reception to leave it. Thank you, from the heart.
      </p>
    </div>

    <div class="maps">"""
    R.append(('    <div class="maps">', GIFT))
    for a, b in R:
        if isinstance(a, str):
            assert a in out, a[:60]
            out = out.replace(a, b, 1)
        else:
            out, n = a.subn(lambda m: b, out, count=1)
            assert n == 1, a.pattern[:60]
    return out
