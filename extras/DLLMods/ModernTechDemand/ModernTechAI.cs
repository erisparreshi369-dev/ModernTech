using UnityEngine;

// Optional companion to the ModernTech data mod: your employees use your own AI coding agent.
//
// When your company has released its own "Coding agent" (the third category of the
// Coding Assistant software type, in-house or for sale) and the boost is switched on,
// software design and development run 100% faster (twice as fast).
//
// Employee effectiveness is recalculated by the game after every work step, so the boost
// goes into the game's own speed multipliers instead: the difficulty's design and
// development speed. The boosted difficulty is a renamed copy ("Medium +AI"), which the
// save keeps, so loading a saved game never applies the boost twice.
//
// It is an option: press Ctrl+Alt+A in game to switch it on or off. The choice is
// remembered globally, so it survives saving, loading and starting a new game.
public class ModernTechAI : ModBehaviour
{
	// 100% faster
	public const float Boost = 2f;

	public const string Marker = " +AI";

	// Where the player's choice is stored (global mod settings, not in the save)
	private const string EnabledKey = "ai-boost-enabled";

	private const string AnnouncedKey = "ai-boost-announced";

	// Only this product unlocks the boost: Coding Assistant -> "Coding agent"
	private const string AgentType = "Coding Assistant";

	private const string AgentCategory = "Coding agent";

	// Player's choice, on by default. A released coding agent is still required on top of it
	private bool _enabled = true;

	// Whether the player has already been told about the boost in this installation
	private bool _announced;

	private float _nextCheck;

	private string _toastText;

	private float _toastUntil;

	private GUIStyle _toastStyle;

	public override void OnActivate()
	{
		_enabled = LoadSetting(EnabledKey, true);
		_announced = LoadSetting(AnnouncedKey, false);
		_nextCheck = 0f;
	}

	public override void OnDeactivate()
	{
		Apply(false);
	}

	private void Update()
	{
		if (Input.GetKey(KeyCode.LeftControl) && Input.GetKey(KeyCode.LeftAlt) && Input.GetKeyDown(KeyCode.A))
		{
			ToggleBoost();
		}
		if (Time.unscaledTime < _nextCheck)
		{
			return;
		}
		_nextCheck = Time.unscaledTime + 2f;
		bool active = _enabled && HasCodingAgent();
		if (active && !_announced)
		{
			_announced = true;
			SaveSetting(AnnouncedKey, true);
			Announce();
		}
		Apply(active);
	}

	// Switch the boost on or off, remembering the choice
	public void ToggleBoost()
	{
		_enabled = !_enabled;
		SaveSetting(EnabledKey, _enabled);
		bool active = _enabled && HasCodingAgent();
		Apply(active);
		Toast(active ? "AI coding agent: employees work 100% faster (Ctrl+Alt+A to switch off)" : "AI coding agent boost switched off (Ctrl+Alt+A to switch on)");
	}

	// The difficulty to switch to, or null when it already matches
	public static DifficultyValues.DifficultySetting Toggle(DifficultyValues.DifficultySetting d, bool boosted)
	{
		string name = d.Name ?? "";
		bool isBoosted = name.EndsWith(Marker);
		if (boosted == isBoosted)
		{
			return null;
		}
		float factor = boosted ? Boost : 1f / Boost;
		DifficultyValues.DifficultySetting copy = new DifficultyValues.DifficultySetting(
			boosted ? name + Marker : name.Substring(0, name.Length - Marker.Length), d);
		copy.AlphaSpeedBonus *= factor;
		copy.DesignDocumentSpeedBonus *= factor;
		return copy;
	}

	// True when the player's company has released its own coding agent
	public static bool HasCodingAgent()
	{
		GameSettings gs = GameSettings.Instance;
		if (gs == null || gs.MyCompany == null || gs.MyCompany.Products == null)
		{
			return false;
		}
		foreach (SoftwareProduct product in gs.MyCompany.Products)
		{
			if (product == null || product.Type == null || product.Category == null)
			{
				continue;
			}
			if (product.Type.Name == AgentType && product.Category.Name == AgentCategory)
			{
				return true;
			}
		}
		return false;
	}

	private void Apply(bool boosted)
	{
		GameSettings gs = GameSettings.Instance;
		if (gs == null || gs.Difficulty == null)
		{
			return;
		}
		DifficultyValues.DifficultySetting next = Toggle(gs.Difficulty, boosted);
		if (next != null)
		{
			gs.Difficulty = next;
		}
	}

	// One-time explanation, the first time the coding agent actually boosts the player
	private void Announce()
	{
		if (WindowManager.Instance == null)
		{
			return;
		}
		WindowManager.Instance.ShowMessageBox(
			"Your employees now use your own AI coding agent. Software design and development run twice as fast.\n\nPress Ctrl+Alt+A to switch the boost off or on again.",
			true,
			DialogWindow.DialogType.Information);
	}

	private void Toast(string text)
	{
		_toastText = text;
		_toastUntil = Time.unscaledTime + 4f;
	}

	private void OnGUI()
	{
		if (_toastText == null || Time.unscaledTime > _toastUntil)
		{
			return;
		}
		if (_toastStyle == null)
		{
			_toastStyle = new GUIStyle(GUI.skin.label);
			_toastStyle.alignment = TextAnchor.MiddleCenter;
			_toastStyle.fontSize = 15;
			_toastStyle.wordWrap = true;
			_toastStyle.normal.textColor = Color.white;
		}
		float width = 520f;
		Rect box = new Rect((Screen.width - width) / 2f, 48f, width, 34f);
		GUI.Box(box, "");
		GUI.Label(new Rect(box.x + 8f, box.y + 4f, width - 16f, 26f), _toastText, _toastStyle);
	}
}
